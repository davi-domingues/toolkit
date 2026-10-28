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

All you need is Node 20+. There is nothing to install.

```bash
git clone https://github.com/davi-domingues/toolkit.git
cd toolkit

node scripts/toolkit.mjs list                  # what exists and where it goes
node scripts/toolkit.mjs install --dry-run     # simulate, touches nothing
node scripts/toolkit.mjs install               # install into every tool
```

## What's inside

| Folder | What it is | Examples |
|---|---|---|
| `skills/` | Capabilities the agent loads on demand (`SKILL.md` + `references/`) | `expo-expert`, `feature-builder`, `java-testing-patterns` |
| `agents/` | Standalone subagents, one `.md` per agent | (coming soon) |
| `rules/` | Always-on global rules | `global.md` |
| `prompts/` | Reusable prompts, exposed as slash commands | `revisar-diff`, `orquestrar` |
| `scripts/` | Installer and validator, plain Node | `toolkit.mjs` |
| `test/` | Installer tests (`node --test`) | |

```
toolkit/
├── skills/<name>/SKILL.md
├── agents/<name>.md
├── rules/<name>.md
├── prompts/<name>.md
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
node scripts/toolkit.mjs list         # assets and their targets
node scripts/toolkit.mjs status       # linked, present or missing, per tool
node scripts/toolkit.mjs install      # --tools kiro,claude  --copy  --dry-run
node scripts/toolkit.mjs uninstall    # removes only what the toolkit installed
node scripts/toolkit.mjs validate     # checks the skills
```

Installer principles:

- **Links by default.** Folders become junctions/symlinks. Files try a symlink and fall back to a copy when permission is missing (Windows).
- **Never overwrites what it doesn't own.** An existing foreign destination is skipped with a warning.
- **Idempotent.** Running it twice changes nothing.
- **Safe uninstall.** It only removes links to this repo or files identical to the ones here. Folders copied with `--copy` are left to you.
- **Zero dependencies.** Node standard library only.

## Adding content

1. Create the file in the right folder. For skills, `skills/<name>/SKILL.md` with `name` equal to the folder name and a `description` that says *when* to use it.
2. Run `npm run validate && npm test`.
3. Note it in `CHANGELOG.md` and open a PR. CI runs validation and tests on Node 20 and 22.

## Roadmap

Ideas and next steps live in [ROADMAP.md](ROADMAP.md).

## Versioning

[SemVer](https://semver.org) in `package.json`, history in the [CHANGELOG](CHANGELOG.md), releases through `vX.Y.Z` tags.

## License

[MIT](LICENSE) © 2026 Davi Domingues
