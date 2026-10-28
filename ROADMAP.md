# Roadmap

A parking lot for ideas and next steps. Nothing here is committed work: items are unrefined until they move out of **Ideas** into **Planned**.

## Planned

_Nothing yet._

## Ideas

### Package and registry

Ship the toolkit as an installable CLI package so a new machine only needs one command. Not refined yet; open questions below.

- Turn the repo into a scoped package (`@davi-domingues/toolkit`) with a `bin` entry and a `files` whitelist (`scripts`, `skills`, `agents`, `rules`, `prompts`). The installer currently finds content from the repo root, so it must read from the package directory instead.
- Publish on tag `vX.Y.Z` through GitHub Actions, checking that the tag matches the `package.json` version and running validate and tests first.
- Registry options:
  - **GitHub Packages (npm):** keeps everything on GitHub and needs no new account. The package follows the repo visibility, and installing needs a token with `read:packages` (to verify: whether fine-grained tokens are accepted).
  - **npmjs.com:** public and installable without a token or `.npmrc`.
- Open questions: which registry, whether the package should be public, and how the first release is cut.

### Other

_Add ideas here._

## Done

See the [CHANGELOG](CHANGELOG.md).
