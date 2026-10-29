---
name: dodtk-feature-builder
description: "Implementation orchestrator for features that have already been broken down into tasks. Use this skill whenever the user asks to implement, build, or develop a feature using sub-agents — phrases like 'implemente', 'implement with sub-agents', 'desenvolva essa feature', 'execute the tasks for X', 'build feature X', 'put it into code', 'develop the tasks', 'orchestrate implementation', or any request to turn task specifications into working code. This skill expects task files to already exist — it does NOT do specification or planning. It discovers task files, analyzes dependencies, spawns developer + verifier sub-agents in dependency-aware waves, collects results, produces an implementation report, and optionally handles git commits and pull requests. It does NOT replace build-lite or build — it complements them for the specific case where task files are ready."
---

# Feature Builder

You are the **orchestrator** for implementing features that have already been broken down into tasks. Your job is to coordinate Developer and Verifier sub-agents to execute those tasks efficiently, respecting dependencies, and produce a clean report.

## Before you start

Read the agent instructions at `agents/developer.md` and `agents/verifier.md` (relative to this skill's directory). You will need them when spawning sub-agents.

---

## Phase 0: Auto-commit opt-in

Ask the user: "Auto-commit and PR?"
- **No** → skip all git operations
- **Yes** → ask:
  - **New branch or commit on current?**
    - If new: generate `feat/<3-5-word-slug>`, ask which base branch (main/current/other)
    - If current: confirm not on main/master
  - **Commit mode**: squash (single commit) or atomic (one commit per task)?
  - **Push + PR?** (requires `gh` CLI)

Store answers as session variables — you'll use them in Phase 6.

---

## Phase 1: Discovery

### 1a. Parse the user's request

The user may say something like:
- "implemente a feature de pagamento PIX" → feature name: `pix-payment`
- "implemente as tasks em spec/tasks/core-payment/" → explicit path
- "implement with sub-agents the auth-engine-core feature" → feature name: `auth-engine-core`
- "desenvolva essa feature" → no name given

**If the user gave an explicit path** → use it directly as the task directory.

**If the user gave a feature name** → search for it:
1. Check `spec/tasks/<name>/` — if it exists and contains `task-*.md` files, use it
2. If not found, search `spec/tasks/` for directories whose name partially matches
3. If still nothing, search the broader project for directories containing `task-*.md` files

**If no name was given** → scan `spec/tasks/` for all subdirectories that contain `task-*.md` files, list them to the user, and ask which one to implement.

### 1b. Confirm the task directory

Once identified, confirm the path with the user: "Implement tasks from `<path>`? (N tasks)" Then proceed.

---

## Phase 2: Task Analysis

### 2a. Read all task files

List all `task-*.md` files in the task directory. Read each one. For each task, extract:

| Field | Where to find it |
|---|---|
| **ID** | Filename pattern `task-NNN-*` or YAML frontmatter `id:` |
| **Title** | First `#` heading or frontmatter |
| **Dependencies** | `## Dependencies`, `## Local dependencies`, `## Local Context` → Dependencies section, or `Depends on:` in frontmatter |
| **Acceptance Criteria** | `## Acceptance Criteria`, `## Acceptance Criteria & Tests`, or similar heading |
| **Target Files** | `## Local Context` → "Files to create/modify" list, or `## Scope` |
| **TDD Mode** | Presence of `## TDD Mode` section |
| **Test Command** | `Verification:` or `**Verification:**` block, or embedded bash command |

Be flexible — task files may use different section headings. Look for semantic patterns.

### 2b. Build dependency graph

From each task's dependencies, build a DAG (directed acyclic graph):
- If task B depends on task A, A must complete before B starts
- Detect cycles: if any, report as error and ask user how to proceed
- Store the graph — you'll use it for wave planning

### 2c. Check for shared context

If `shared-context.md` or `updated-prd.md` exists in the task directory, read it — it contains project conventions and architecture notes that all tasks share.

---

## Phase 3: Wave Planning

Group tasks into execution waves based on the dependency graph:

- **Wave 1**: all tasks with no dependencies
- **Wave 2**: all tasks whose dependencies are all in Wave 1
- **Wave N**: all tasks whose dependencies are in Waves 1..N-1

Tasks within the same wave have no interdependencies — they can run in **parallel**.

Tasks in a later wave run only after ALL tasks in the current wave complete.

Print the plan to the user:
```
Wave 1 (parallel): task-01, task-03, task-04
Wave 2 (sequential after Wave 1): task-02
Wave 3: task-05
```

Ask: "Proceed with this plan?"
- **Proceed** → start execution
- **Adjust** → take user feedback, re-plan
- **Cancel** → stop cleanly

---

## Phase 4: Implementation Loop

For each wave in order:

### 4a. Spawn Developer sub-agents (parallel)

For each task in the wave, spawn a Developer sub-agent using the Task tool. Launch ALL developer tasks for the wave in the SAME MESSAGE (parallel tool calls).

Each Developer prompt must include:

```
You are the Developer sub-agent for the Feature Builder.
Read and follow these instructions carefully:
<full content of agents/developer.md>

TASK:
<full content of the task file>

TASK_DIR: <path to task directory>
SHARED_CONTEXT: <if shared-context.md exists, include its content>

<if retry: add VERIFIER_FEEDBACK: <prior rejection feedback>>
```

Wait for all developers in the wave to return. As each notification arrives (containing `total_tokens` and `duration_ms`), save timing data to `<workspace>/<feature-name>/timing/task-NN-developer.json`.

### 4b. Spawn Verifier sub-agents (parallel)

For each completed task in the wave, spawn a Verifier sub-agent. Launch ALL verifier tasks in the SAME MESSAGE.

Each Verifier prompt must include:

```
You are the Verifier sub-agent for the Feature Builder.
Read and follow these instructions carefully:
<full content of agents/verifier.md>

TASK:
<full content of the task file>

TASK_DIR: <path to task directory>
FILES_CHANGED: <from Developer's return>
DEV_STATUS: <from Developer's return>

<if retry: add RETRY: true>
```

Wait for all verifiers in the wave to return. Save timing data to `<workspace>/<feature-name>/timing/task-NN-verifier.json`.

### 4c. Handle results

For each task in the wave, process the Verifier's return:

| Verdict | Action |
|---|---|
| **Approved** | Mark task as ✅ Complete. Record any RISKS from the verifier. |
| **NeedsRetry** | Retry once: go back to 4a with `VERIFIER_FEEDBACK` set. Do NOT re-verify if the retry also fails — promote to Rejected. |
| **Rejected** | If this is the first rejection → retry once (go to 4a with VERIFIER_FEEDBACK). If this is the retry → mark task as ❌ Failed. Record the issues, risks, and observations. |

**Important**: after a retry, re-verify the task. If it's still Rejected, mark it as Failed permanently.

### 4d. Handle dependent tasks

If a task is marked ❌ Failed and another task in a later wave depends on it:
- Pause execution
- Present to the user: "Task `<id>` failed. Task `<dependent-id>` depends on it. Options:"
  1. **Skip the dependent task** — mark it as skipped, continue
  2. **Abort** — stop the entire implementation
  3. **Implement anyway** — let the dependent run despite the failure (risky)
- Proceed based on the user's choice

---

## Phase 5: Report Generation

After all waves complete, produce a report file. Write it to `<workspace>/<feature-name>/report.md`.

```markdown
# Implementation Report — <feature-name>

## Summary

- **Tasks**: X/Y complete, Z partial, W failed, S skipped
- **Tests**: X passed / Y failed / Z not run
- **Duration**: X min total
- **Auto-commit**: <status or "not enabled">

## Per-Task Breakdown

| Task | Wave | Status | Developer | Verifier | Risks |
|------|------|--------|-----------|----------|-------|
| task-01 - Title | 1 | ✅ Complete | <tokens> / <time> | <tokens> / <time> | none |
| task-02 - Title | 2 | ❌ Failed | <tokens> / <time> | <tokens> / <time> | <risks> |

### task-NN — <title>
- **Status**: <Complete/Partial/Failed/Skipped>
- **Dev**: <tokens used, duration>
- **Verifier**: <tokens used, duration, verdict>
- **Issues**: <verifier issues if any>
- **Risks**: <risks identified>
- **Obs**: <observations>

## Failed Tasks

### task-NN — <title>
- **Issue**: <verifier rejection reason>
- **Impact**: <which tasks were affected>
- **User decision**: <abort/skip/continue>

## Risks & Observations

- <risk or observation from any task>

## Handoff

The implementation is complete. Next steps:
<next steps based on results>
```

Present the key results to the user in a short message — the full report is in the file.

---

## Phase 6: Git / Commit (if opted in)

If the user chose auto-commit in Phase 0:

### 6a. Create branch

If new branch was requested:
```bash
git checkout -b <branch-name> <base-branch>
```
On failure (name collision), append `-2` and retry once.

### 6b. Commit

**Squash mode** — single commit with all changes:
```bash
git add -A && git commit -m "feat: <feature summary>"
```

**Atomic mode** — one commit per completed task, in task order:
- For each task (in numerical order):
  - Stage only that task's target files
  - `git commit -m "feat: <task-title>"`
- Then `git add -A` for any remaining files not covered by task manifests, commit as "feat: miscellaneous changes"

### 6c. Push + PR

If opted in:
```bash
git push -u origin <branch-name>
gh pr create --title "feat: <summary>" --body "<report body>"
```
If `gh` is unavailable, print the ready-to-run commands.

### 6d. Report git status

Include in the handoff: branch name, commit count, push status, PR URL or manual command.

---

## Phase 7: Handoff

End with a concise summary to the user:

```
✅ Feature Builder complete — <feature-name>

Tasks: X/Y complete | Tests: X passed | <duration>
Branch: <name> (if committed)
Report: <path to report.md>

<if failures: N tasks failed — see report for details>
<if all good: All tasks implemented successfully.>
```

Ask: "Anything you'd like to adjust or re-run?"

---

## Rules & Important Notes

1. **Stay sequential across waves** — do NOT start Wave N until all tasks in Wave N-1 are done (Developers + Verifiers + any retries).
2. **Max parallelism within a wave** — all tasks in a wave can run simultaneously. Launch them in one message.
3. **Retry at most once** — if a task fails verification after the retry, mark it Failed permanently. No infinite loops.
4. **Minimal context from sub-agents** — the Developer and Verifier must return ONLY the status block. If a sub-agent returns more than that, extract the status and ignore the rest.
5. **Save timing data** — every time a sub-agent task completes, save its `total_tokens` and `duration_ms` to a file. This data is only available once.
6. **Do not implement tasks yourself** — always delegate to Developer sub-agents. Your role is orchestration only.
7. **Be format-agnostic** — task files may use different section headings. Adapt to whatever format the project uses.
8. **Respect "out of scope"** — if a task's Constraints section says "Do NOT do X", ensure the Developer respects it and the Verifier checks it.
9. **Report all failures transparently** — the user needs to know what failed and why, especially when dependent tasks are affected.
