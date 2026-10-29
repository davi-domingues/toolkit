<div align="center">

# toolkit

**My toolbox for AI coding agents.**
Skills, agents, rules and prompts in one place, versioned and installed with a single command.

![node](https://img.shields.io/badge/node-%3E%3D20-339933?logo=node.js&logoColor=white)
![deps](https://img.shields.io/badge/dependencies-0-brightgreen)
![tools](https://img.shields.io/badge/Kiro%20%7C%20Claude%20Code%20%7C%20OpenCode-supported-blue)
![license](https://img.shields.io/badge/license-MIT-blue)

</div>

---

## Why this exists

Every AI agent keeps its instructions somewhere different: `~/.kiro/steering`, `~/.claude/rules`, `~/.config/opencode/commands`... Copying files by hand between folders drifts within a week.

The toolkit fixes that with one simple rule: **a single source, many targets**. You edit here, and the installer links the files where each tool expects them. Change a file in the repo and it changes everywhere.

## Quick start

Requires Node 20+. The package is published to GitHub Packages, which requires a token even to install public packages.

1. Create a [personal access token (classic)](https://github.com/settings/tokens/new?scopes=read:packages) with only the `read:packages` scope. GitHub Packages does not accept fine-grained tokens.
2. Point the scope at GitHub Packages and save the token in your user `~/.npmrc` (never in the repo):

   ```bash
   npm config set @davi-domingues:registry https://npm.pkg.github.com
   npm config set //npm.pkg.github.com/:_authToken <TOKEN>
   ```

3. Install and run:

   ```bash
   npm i -g @davi-domingues/toolkit

   dod-toolkit list                  # what exists and where it goes
   dod-toolkit install --dry-run     # simulate, touches nothing
   dod-toolkit install               # install into every tool
   ```

Links point into the installed package, so `npm i -g @davi-domingues/toolkit@latest` updates every tool at once. Run `dod-toolkit install` again to pick up new assets, and `dod-toolkit uninstall` before `npm uninstall -g` so no broken links are left behind.

The command is `dod-toolkit` and every asset is prefixed with `dodtk-`, so this toolkit can live next to other toolkits that install a `toolkit` command or same-named skills.

**Upgrading from 0.2.0:** that version used the `toolkit` command and unprefixed names. Run `toolkit uninstall` with 0.2.0 first, then upgrade and run `dod-toolkit install`.

### From a clone

To work on the toolkit itself, clone it and use the same commands through `node bin/toolkit.js`:

```bash
git clone https://github.com/davi-domingues/toolkit.git
cd toolkit
node bin/toolkit.js install
```

## What's inside

| Folder | What it is | Examples |
|---|---|---|
| `skills/` | Capabilities the agent loads on demand (`SKILL.md` + `references/`) | `dodtk-expo-expert`, `dodtk-feature-builder`, `dodtk-java-testing-patterns` |
| `agents/` | Standalone subagents, one `.md` per agent | (coming soon) |
| `rules/` | Always-on global rules | `dodtk-global.md` |
| `prompts/` | Reusable prompts, exposed as slash commands | `dodtk-revisar-diff`, `dodtk-orquestrar` |
| `bin/` | CLI entry point (`dod-toolkit`) | `toolkit.js` |
| `scripts/` | Installer and validator, plain Node | `toolkit.mjs` |
| `test/` | Installer tests (`node --test`) | |

```
toolkit/
├── skills/<name>/SKILL.md
├── agents/<name>.md
├── rules/<name>.md
├── prompts/<name>.md
├── bin/toolkit.js
├── scripts/toolkit.mjs
└── test/
```

## Where everything goes

| Tool | skills | agents | rules | prompts |
|---|---|---|---|---|
| **Kiro** | `~/.kiro/skills` | | `~/.kiro/steering` | `~/.kiro/prompts` |
| **Claude Code** | `~/.claude/skills` | `~/.claude/agents` | `~/.claude/rules` | `~/.claude/commands` |
| **OpenCode** | `~/.config/opencode/skills` | | | `~/.config/opencode/commands` |

`rules/` is the neutral name: Kiro calls it *steering*, Claude Code calls it *rules*. Tools that only read a single `AGENTS.md` are left out on purpose, the toolkit does not generate concatenated files.

## Commands

```bash
dod-toolkit list         # assets and their targets
dod-toolkit status       # linked, present or missing, per tool
dod-toolkit install      # --tools kiro,claude  --copy  --dry-run
dod-toolkit uninstall    # removes only what the toolkit installed
dod-toolkit validate     # checks the skills
dod-toolkit --help       # usage, version, author and license
```

Installer principles:

- **Links by default.** Folders become junctions/symlinks. Files try a symlink and fall back to a copy when permission is missing (Windows).
- **Never overwrites what it doesn't own.** An existing foreign destination is skipped with a warning.
- **Idempotent.** Running it twice changes nothing.
- **Safe uninstall.** It only removes links to this repo or files identical to the ones here. Folders copied with `--copy` are left to you.
- **Zero dependencies.** Node standard library only.

## Adding content

1. Create the file in the right folder, with a name starting with `dodtk-`. For skills, `skills/dodtk-<name>/SKILL.md` with `name` equal to the folder name and a `description` that says *when* to use it. `validate` fails on any asset without the prefix.
2. Run `npm run validate && npm test`.
3. Note it in `CHANGELOG.md` and open a PR. CI runs validation and tests on Node 20 and 22.

## Roadmap

Ideas and next steps live in [ROADMAP.md](ROADMAP.md).

## Versioning

[SemVer](https://semver.org) in `package.json`, history in the [CHANGELOG](CHANGELOG.md). The pull request and release process is in [CONTRIBUTING](CONTRIBUTING.md).

## License

[MIT](LICENSE) © 2026 Davi Domingues
