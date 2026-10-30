---
name: dodtk-create-commit
description: Prepares and creates git commits in Conventional Commits, pt-BR ASCII, with the ticket key (Jira, Linear, etc.) as scope when the repo uses tickets (feat(SA-156): ...) and without scope when it does not (feat: ...). Use when the user asks to commit changes, "faz o commit", "commita", "gera a mensagem de commit", split or group commits, stage files, or organize changes before commit. Never pushes, never commits on main/develop/master.
---
# Create Commit

Prepares one commit per relevant block of changes, grouped by context, and creates it according to the commit mode chosen in the session. Never pushes: push is a separate step, done by the user or by a pull/merge request flow, always with approval.

## Required input

| Input | How to get it |
|---|---|
| Repo and diff | Current directory. Read-only commands (`git status`, `git diff`, `git branch --show-current`, `git log`) are always allowed. |
| Commit mode | Ask the user (see Step 1). Never assume. |
| Ticket key `XX-NN` | Infer from the branch `<tipo>/<XX-NN>_<slug>` (regex `[A-Z]+-\d+`; branch type is open). If it cannot be inferred, see Step 2. |
| Intent of the change | The user's description and the diff. If the purpose is unclear, ask. |

## Steps

1. **Commit mode.** Before the first commit of the session, ask which mode to use and remember it until the end:
   - a) Approve each commit one by one: show the proposal (title, body and files) and wait before staging and committing.
   - b) Approve all next commits of the session: stage and commit every proposed group without asking again.
   - c) Outside the workflow: only propose the text; no `git add`, no `git commit`.

   Ask again when the demand or repo changes, or if the user revokes the choice.
2. **Preconditions.** Details and error handling in [references/checks-and-errors.md](references/checks-and-errors.md).
   - Current branch is `main`, `develop` or `master`: stop and warn. Create the demand branch first.
   - Ticket: use the key from the branch name. If the branch has no key, check the repo conventions (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `git log`). If they do not settle it, ask whether the repo uses tickets. Repo with tickets: ask for the `XX-NN` key. Repo without tickets: commit without scope. Remember the answer per repo for the session.
   - Diff with new ordinary code comments or secrets: warn BEFORE committing, with file and line; proceed only with explicit user approval, even in mode b.
3. **Group.** Split changes by top-level folder or feature, ordered from foundational to surface. Stage only the group's files with explicit paths (`git add -p` when a file mixes contexts). No `git add -A` unless the user asked to commit everything.
4. **Write the message** following [references/commit-template.md](references/commit-template.md).
   - With ticket: `<tipo>(<XX-NN>): <descricao curta>`.
   - Without ticket: `<tipo>: <descricao curta>`.
   - pt-BR plain ASCII, third person present indicative, fits "Se aplicado, este commit: <titulo>", at most 72 characters.
   - Body: one to three short sentences, then bullets with the macro changes.
   - If the repo documents a different commit convention, it prevails: follow it and say so in the proposal.
5. **Execute.**
   - Mode a or b: `git add` the group's files and `git commit` with title and body (after approval in a; directly in b). If a hook fails, fix the cause and create a new commit.
   - Mode c: only output the proposal.
6. **Report** in the formats of [references/commit-template.md](references/commit-template.md).

## Done when

- Every change of the requested scope is in a commit (or, in mode c, in a proposal), with no unrelated file staged.
- Each title follows the format, the ASCII rule and the 72-character limit.
- No new code comment or secret was committed without explicit approval.
- Nothing was pushed.

## Constraints

- Never `git push`, `--force` or `--no-verify`. Never `--amend` unless the user asks explicitly.
- Never commit on `main`, `develop` or `master`.
- Never force a ticket key: when it cannot be inferred, ask.
- When only proposing or reporting, output just what the template defines; questions and warnings are separate messages.
