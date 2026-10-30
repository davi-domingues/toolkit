# Preconditions and Error Handling

## Preconditions

1. **Protected branch.** If `git branch --show-current` returns `main`, `develop` or `master`, stop. Warn that commits there are not allowed and that the demand must be on a branch named `<tipo>/<XX-NN>_<slug>` (or `<tipo>/<slug>` in repos without tickets).
2. **Ticket key.**
   - Branch `<tipo>/<XX-NN>_<slug>` (branch type is open: `feature`, `bugfix`, `refactor`, `hotfix`, ...): the key matches `[A-Z]+-\d+` (e.g. `SA-156`, `PSA-1983`, `INCSA-29`). Use it as scope.
   - Key not inferable: look for the convention in `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` and recent `git log` titles. If still unclear, ask "Este repo usa ticket nos commits (ex.: SA-156) ou nao?". Repo with tickets: ask for the `XX-NN` key. Repo without tickets: title without parentheses.
   - Personal, tooling and documentation repos usually have no tickets, but confirm instead of assuming.
3. **Blocking rules.** The diff must not add:
   - ordinary code comments (doc comments on public API, such as Javadoc, JSDoc or docstrings, are allowed when the repo uses them);
   - secrets (tokens, passwords, keys, `.env` files).

   If it does, warn BEFORE committing pointing out file and line, and proceed only with the user's explicit approval, even in mode b. Record the decision in the commit body only if the user asks. Rules in the repo's `AGENTS.md` or `CLAUDE.md` add to these.

## Staging policy

- Stage only the files of the group being committed, with explicit paths.
- Mixed contexts in one file: `git add -p`.
- Mode a: list the files in the proposal so the approval covers staging.
- `git add -A` only when the user asked to commit everything.

## Known errors

| Situation | Handling |
|---|---|
| No changes in `git status` | Report that there is nothing to commit; do not create an empty commit. |
| Files already staged by the user | Show them and ask whether they belong to the group; do not unstage silently. |
| Detached HEAD | Stop and ask the user for the branch to use. |
| Hook fails | Fix the cause, re-stage and create a NEW commit. Never `--no-verify`, never `--amend` unless asked. |
| Title above 72 characters | Shorten the description; do not drop the type or the scope. |
| Description in imperative or past (`remova`, `removido`) | Rewrite in third person present (`remove`). |
| User asks to push or open a PR/MR | Refuse to push in this skill; say push is a separate step that needs its own approval. |
| Branch named `main`/`develop`/`master` after mode b was approved | Mode does not override the rule; stop. |
