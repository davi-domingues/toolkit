---
name: dodtk-readme-refresh
description: Analisa um repositório, reescreve o README com a arquitetura real (AS IS), faz commit no padrão do repo e push. Use quando o usuário pedir para atualizar, reescrever, refazer ou documentar o README de um projeto, ou deixar o README fiel ao código. Uso - /dodtk-readme-refresh <caminho> [destaque: <tema>] [--auto]
---

# README Refresh

Argumentos recebidos: $ARGUMENTS

## Interpretação dos argumentos

- **Caminho**: diretório do repositório. Se ausente, use o diretório atual.
- **`destaque: <tema>`** (opcional): assunto que deve ficar fácil de encontrar no README (ex.: "SQS na parte de notificação"). Destaque de forma natural, sem quebrar o fluxo de um README comum.
- **`--auto`** (opcional): faça commit e push direto na branch atual, sem pedir confirmação. Sem essa flag, mostre o diff e a mensagem de commit e aguarde aprovação antes de commitar/pushar.

## Regras

- Documente o projeto **AS IS**. Não altere código, configs ou outros docs. Inconsistências encontradas (portas divergentes, exemplos errados, bugs) são apenas listadas no resumo final, nunca corrigidas.
- Toda afirmação no README deve vir de algo lido (código, configs, compose, scripts, docs). O que não puder ser confirmado fica fora do README ou é dito com cautela, e é mencionado no resumo como não verificado.
- Nunca copie valores de segredos (senhas, tokens, chaves) para o README. Cite apenas o nome da variável/arquivo.
- Escreva no idioma do README/docs existentes.
- Sem emojis decorativos, sem seções vazias ou boilerplate. Tamanho proporcional ao projeto.

## Fluxo

### 1. Reconhecimento

No diretório do repo, em paralelo:
- `git status --short`, `git branch --show-current`, `git log --oneline -10`, `git remote -v`
- Listagem recursiva do diretório (ignorando `node_modules`, `target`, `.git`, `dist`, `build`)

Se houver alterações não commitadas fora do README, não as inclua no commit e avise no resumo.

### 2. Análise

Leia o README atual e os arquivos que definem a arquitetura real:
- Build/módulos: `pom.xml`, `package.json`, `build.gradle`, `Cargo.toml`, `requirements.txt` etc.
- Infra: `docker-compose*.yml`, `Dockerfile*`, scripts de setup (`*.sh`, `*.ps1`), IaC
- Configs de exemplo: `application.properties.example`, `.env.example`
- Pontos de entrada, controllers/rotas, clientes HTTP, integrações (filas, e-mail, banco)
- Docs existentes: ADRs, `docs/`, guias

Para repositórios grandes, delegue a leitura a um sub-agente e peça um relatório com: módulos, portas, dependências entre serviços, infraestrutura, fluxo de execução e o tema de destaque.

Levante: componentes e responsabilidades, portas, comunicação entre componentes, stack com versões, como executar e onde estão os arquivos-chave do tema de destaque.

### 3. Escrita do README

Estrutura base (adapte ao projeto, omita o que não se aplica):

1. Título + descrição curta (preserve o contexto original do projeto, se houver)
2. **Arquitetura**: diagrama Mermaid (`flowchart LR`) + tabela de componentes (nome, porta, responsabilidade)
3. **Seção do tema de destaque** (se informado): logo após a arquitetura, com título explícito contendo o nome da tecnologia; fluxo em passos numerados, tabela se fizer sentido e "onde encontrar no código" com links relativos para os arquivos
4. **Tecnologias**
5. **Como executar**: pré-requisitos, infraestrutura, configuração, build e execução, com comandos reais do projeto
6. **Documentação**: links para docs existentes
7. Observações relevantes (ex.: credenciais fixas em arquivos, sem expor valores)

Para o tema de destaque aparecer sem forçar: cite-o uma vez na descrição inicial, mostre-o no diagrama e dê a ele uma seção própria. Não repita em toda seção.

Depois de escrever, releia o README contra o código para confirmar portas, nomes, caminhos e comportamentos descritos. Confira se todos os links relativos apontam para arquivos existentes.

### 4. Commit

- Descubra a convenção de mensagens no `git log` (Conventional Commits, gitmoji como `:memo: docs: ...`, idioma, formato `escopo | descrição`) e siga-a. Para mudanças só de documentação, use o tipo `docs`.
- Mensagem: título curto + corpo com 2 a 4 bullets do que mudou.
- Adicione apenas o `README.md` (`git add README.md`), nunca `git add .`.

**Sem `--auto`**: mostre `git diff --stat`, a mensagem proposta, a branch atual e o remoto. Se a branch for `main`/`master`, pergunte se o push vai direto nela ou numa branch nova com PR. Aguarde confirmação.

**Com `--auto`**: rode os comandos em sequência, nunca em paralelo com edições de arquivo:

```bash
git add README.md
git commit -m "<título>" -m "<corpo>"
git push origin <branch-atual>
```

Nunca use `--force`, `--no-verify` ou `--amend`. Se o push for rejeitado (ex.: remoto à frente), pare e reporte; não faça rebase/merge automático.

### 5. Verificação

- `git status --short` deve estar limpo em relação ao README.
- `git show HEAD:README.md` deve conter o conteúdo final (confira trechos editados por último).
- Confirme a saída do push (`<old>..<new> <branch> -> <branch>`).

### 6. Resumo final

Em poucas frases: hash do commit, branch, o que o README passou a cobrir, onde está o tema de destaque, inconsistências encontradas (não corrigidas) e afirmações não verificadas.
