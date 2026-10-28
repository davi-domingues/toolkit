# toolkit

Meu toolkit pessoal de **skills, agents e steering** para agentes de IA (Kiro, Claude Code, OpenCode). Uma fonte única versionada, instalada nas ferramentas por link, sem copiar à mão.

> Este repo é independente do toolkit do GitLab corporativo: conteúdo e assets são mantidos separadamente.

## Estrutura

```
skills/<nome>/SKILL.md      skill (frontmatter name == pasta, description com gatilhos) + references/
agents/<nome>.md            subagents standalone
steering/<nome>.md          regras globais
scripts/toolkit.mjs         instalador/validador (Node, sem dependências)
test/                       testes do instalador (node --test)
```

Skills atuais: `expo-expert`, `feature-builder`, `java-testing-patterns`.

## Destinos

| Ferramenta | skills | agents | steering |
|---|---|---|---|
| kiro | `~/.kiro/skills` | - | `~/.kiro/steering` |
| claude | `~/.claude/skills` | `~/.claude/agents` | - |
| opencode | `~/.config/opencode/skills` | - | - |

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
- Arquivos (agents/steering) tentam symlink; sem permissão, caem para cópia.
- Destino existente que não seja deste toolkit é **pulado**, nunca sobrescrito.
- `uninstall` remove apenas links para este repo (ou arquivos idênticos aos daqui). Cópias de pastas feitas com `--copy` devem ser removidas manualmente.

## Adicionar conteúdo

1. Crie `skills/<nome>/SKILL.md` com `name` igual à pasta e `description`.
2. `npm run validate && npm test`.
3. Registre no `CHANGELOG.md`, abra PR; o CI roda validação e testes.

## Versionamento

SemVer em `package.json`, histórico no `CHANGELOG.md`, release por tag `vX.Y.Z`.
