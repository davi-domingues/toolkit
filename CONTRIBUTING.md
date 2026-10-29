# Contributing

`main` is protected by a ruleset: no direct pushes, no force pushes, linear history, and the `ci` checks must pass. Every change, including releases, goes through a pull request.

## Changing the toolkit

1. Branch from an up-to-date `main`: `git switch -c feat/<short-name>`.
2. Make the change. New assets must start with `dodtk-` (see "Adding content" in the [README](README.md)).
3. Run `npm run validate && npm test`.
4. Add a line under `## Unreleased` in [CHANGELOG.md](CHANGELOG.md).
5. Push and open a pull request. Merge with **squash** once CI is green.

## Releasing

The `publish` workflow runs when a `vX.Y.Z` tag is pushed. Tags are protected, so a published tag cannot be moved or deleted, and the version bump reaches `main` through a pull request before the tag is created.

1. Create a release branch and bump the version without tagging:

   ```bash
   git switch main && git pull
   git switch -c release/X.Y.Z
   npm version <patch|minor|major> --no-git-tag-version
   ```

2. In `CHANGELOG.md`, rename `## Unreleased` to `## X.Y.Z` and open a new empty `## Unreleased` above it.
3. Commit as `chore: release X.Y.Z`, push, open a pull request and squash-merge it after CI passes.
4. Tag the merge commit on `main` and push the tag:

   ```bash
   git switch main && git pull
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

5. The workflow checks that the tag matches `package.json`, runs validate and tests, publishes to GitHub Packages and creates the GitHub Release. The `release` environment may ask for your approval before the job starts.

If the workflow fails before `npm publish`, fix the problem through a new pull request and release the next patch version. Do not move the tag.
