# toolkit

Meu toolkit pessoal de **skills, agents e steering** para agentes de IA (Kiro, Claude Code, OpenCode). Uma fonte única versionada, instalada nas ferramentas por link, sem copiar à mão.

> Este repo é independente do toolkit do GitLab corporativo: conteúdo e assets são mantidos separadamente.

## Estrutura

```
skills/<nome>/SKILL.md      skill (frontmatter name == pasta, description com gatilhos) + references/
agents/<nome>.md            subagents standalone
rules/<nome>.md             regras globais (instrucoes sempre ativas)
prompts/                    prompts reutilizaveis (nao instalados; uso manual)
scripts/toolkit.mjs         instalador/validador (Node, sem dependências)
test/                       testes do instalador (node --test)
```

Skills atuais: `expo-expert`, `feature-builder`, `java-testing-patterns`.

## Destinos

| Ferramenta | skills | agents | rules |
|---|---|---|---|
| kiro | `~/.kiro/skills` | - | `~/.kiro/steering` |
| claude | `~/.claude/skills` | `~/.claude/agents` | `~/.claude/rules` |
| opencode | `~/.config/opencode/skills` | - | - |

`rules/` é o nome neutro: cada ferramenta o chama de um jeito (steering no Kiro, rules no Claude Code). Codex, OpenCode, Copilot e Gemini leem um único arquivo (`AGENTS.md`/`GEMINI.md`), não uma pasta, por isso ainda não são alvo de rules.

## Uso

Requer Node 20+.

```bash
node scripts/toolkit.mjs install --dry-run          # simula
node scripts/toolkit.mjs install                    # linka em todas as ferramentas
node scripts/toolkit.mjs install --tools kiro       # só no Kiro
node scripts/toolkit.mjs status                     # linkado / presente / ausente
node scripts/toolkit.mjs uninstall                  # remove só o que o toolkit instalou
node scripts/toolkit.mjs validate                   # valida as skills
```

Comportamento:
- Skills (pastas) viram junction/symlink: editar no repo reflete na hora.
- Arquivos (arquivos de agents/rules) tentam symlink; sem permissão, caem para cópia.
- Destino existente que não seja deste toolkit é **pulado**, nunca sobrescrito.
- `uninstall` remove apenas links para este repo (ou arquivos idênticos aos daqui). Cópias de pastas feitas com `--copy` devem ser removidas manualmente.

## Adicionar conteúdo

1. Crie `skills/<nome>/SKILL.md` com `name` igual à pasta e `description`.
2. `npm run validate && npm test`.
3. Registre no `CHANGELOG.md`, abra PR; o CI roda validação e testes.

## Versionamento

SemVer em `package.json`, histórico no `CHANGELOG.md`, release por tag `vX.Y.Z`.
