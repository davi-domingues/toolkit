<div align="center">

# toolkit

**Minha caixa de ferramentas para agentes de IA.**
Skills, agents, rules e prompts em um só lugar, versionados e instalados com um comando.

![node](https://img.shields.io/badge/node-%3E%3D20-339933?logo=node.js&logoColor=white)
![deps](https://img.shields.io/badge/dependencias-0-brightgreen)
![ferramentas](https://img.shields.io/badge/Kiro%20%7C%20Claude%20Code%20%7C%20OpenCode-suportados-blue)

</div>

---

## Por que isso existe

Cada agente de IA guarda suas instruções num lugar diferente: `~/.kiro/steering`, `~/.claude/rules`, `~/.config/opencode/commands`... Copiar arquivo à mão entre pastas dá drift em uma semana.

O toolkit resolve isso com uma regra simples: **uma fonte única, vários destinos**. Você edita aqui, o instalador linka onde cada ferramenta espera. Mudou o arquivo no repo, mudou em todo lugar.

## Início rápido

Precisa só do Node 20+. Não há nada para instalar.

```bash
git clone https://github.com/davi-domingues/toolkit.git
cd toolkit

node scripts/toolkit.mjs list                  # o que existe e para onde vai
node scripts/toolkit.mjs install --dry-run     # simula, não toca em nada
node scripts/toolkit.mjs install               # instala em todas as ferramentas
```

## O que tem dentro

| Pasta | O que é | Exemplos |
|---|---|---|
| `skills/` | Capacidades que o agente carrega sob demanda (`SKILL.md` + `references/`) | `expo-expert`, `feature-builder`, `java-testing-patterns` |
| `agents/` | Subagents standalone, um `.md` por agent | (em breve) |
| `rules/` | Regras globais sempre ativas | `global.md` |
| `prompts/` | Prompts reutilizáveis, viram slash commands | `revisar-diff`, `orquestrar` |
| `scripts/` | Instalador e validador, Node puro | `toolkit.mjs` |
| `test/` | Testes do instalador (`node --test`) | |

```
toolkit/
├── skills/<nome>/SKILL.md
├── agents/<nome>.md
├── rules/<nome>.md
├── prompts/<nome>.md
├── scripts/toolkit.mjs
└── test/
```

## Para onde cada coisa vai

| Ferramenta | skills | agents | rules | prompts |
|---|---|---|---|---|
| **Kiro** | `~/.kiro/skills` | | `~/.kiro/steering` | `~/.kiro/prompts` |
| **Claude Code** | `~/.claude/skills` | `~/.claude/agents` | `~/.claude/rules` | `~/.claude/commands` |
| **OpenCode** | `~/.config/opencode/skills` | | | `~/.config/opencode/commands` |

`rules/` é o nome neutro: o Kiro chama de *steering*, o Claude Code de *rules*. Ferramentas que só leem um `AGENTS.md` único ficam de fora de propósito, o toolkit não gera arquivos concatenados.

## Comandos

```bash
node scripts/toolkit.mjs list         # assets e destinos
node scripts/toolkit.mjs status       # linkado, presente ou ausente, por ferramenta
node scripts/toolkit.mjs install      # --tools kiro,claude  --copy  --dry-run
node scripts/toolkit.mjs uninstall    # remove só o que o toolkit instalou
node scripts/toolkit.mjs validate     # confere as skills
```

Princípios do instalador:

- **Link por padrão.** Pastas viram junction/symlink. Arquivos tentam symlink e, sem permissão (Windows), caem para cópia.
- **Nunca sobrescreve o que não é dele.** Destino existente e alheio é pulado com aviso.
- **Idempotente.** Rodar duas vezes não muda nada.
- **Desinstala com segurança.** Só remove links para este repo ou arquivos idênticos aos daqui. Pastas copiadas com `--copy` ficam por sua conta.
- **Zero dependências.** Só a biblioteca padrão do Node.

## Adicionando conteúdo

1. Crie o arquivo na pasta certa. Para skills, `skills/<nome>/SKILL.md` com `name` igual ao nome da pasta e uma `description` que diga *quando* usar.
2. `npm run validate && npm test`
3. Anote no `CHANGELOG.md` e abra um PR. O CI roda validação e testes no Node 20 e 22.

## Versionamento

[SemVer](https://semver.org/lang/pt-BR/) em `package.json`, histórico no [CHANGELOG](CHANGELOG.md), releases por tag `vX.Y.Z`.

## Licença

Uso pessoal. Fique à vontade para pegar a ideia e montar o seu.
