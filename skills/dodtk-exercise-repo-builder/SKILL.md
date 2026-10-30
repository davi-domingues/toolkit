---
name: dodtk-exercise-repo-builder
description: Cria um repositório de exercício/treino pronto para começar (estilo GitHub Classroom), a partir de uma ideia descrita pelo usuário em mensagem ou arquivo. Gera enunciado (README com contexto, regras, passo a passo e cenários), código starter que compila mas não pontua, testes de asserção com fixtures, autograding.json com pontos, pipeline de CI e runner local de nota. Agnóstico de linguagem, framework e plataforma (Java, Node/TS, Python, .NET, Go, Rust, PHP, front-end, SQL, infra...). Use quando o usuário pedir para criar exercício, atividade, desafio, kata, lista de exercícios, prova prática, treino, dojo, repo de prática com testes/correção automática, ou para "transformar esta ideia em um exercício".
license: MIT
compatibility: kiro-cli, opencode, claude-code, codex, cursor
metadata:
  version: "1.0.0"
  language: pt-BR
---

# Exercise Repo Builder

Transforma uma ideia de treino em um repositório no padrão "template de exercício + correção automática": o aluno faz fork (ou branch), implementa, dá push e o pipeline calcula a nota rodando testes já escritos.

Recursos desta skill (carregue **só quando o passo pedir**):

| Arquivo | Quando ler |
|---------|------------|
| `references/anatomy.md` | Sempre no 1º uso: estrutura e ciclo de vida que o repo deve ter |
| `references/exercise-types.md` | Passo 2 — escolher tipo (implement, katas, write-tests, fix-bug, project) |
| `references/assertion-strategies.md` | Passo 2 — escolher como verificar cada objetivo |
| `references/stacks/<stack>.md` | Passo 4 — seletores, libs de teste, fixtures e idioms da stack (`java-spring`, `node`, `python`, `dotnet`, `go`, `others`) |
| `references/grading-pipeline.md` | Passo 6 — formato do autograding.json, CI, fork vs branch |
| `references/authoring-checklist.md` | Passo 7 — revisão final e anti-padrões |
| `references/examples-catalog.md` | Opcional — exemplos reais analisados, para calibrar tamanho/pontuação |
| `templates/spec.md` | Passo 1 — rascunho interno da especificação |
| `templates/readme/<tipo>.md`, `templates/RUBRICA.md`, `templates/autograding.json`, `templates/ci/*` | Usados pelo `scaffold.py`; edite o resultado gerado, não os templates |
| `scripts/scaffold.py` | Passo 3 — gera a casca do repo |
| `scripts/grade.py` | Runner de nota (copiado para o repo) |
| `scripts/integrity.py` | Gate anti-alteração de testes (copiado para o repo) |
| `scripts/verify.py` | Passo 7 — prova que starter = 0% e gabarito = 100% |

`<SKILL_DIR>` = pasta deste arquivo. Scripts exigem Python 3.8+ (stdlib). No Windows use `python`; em Linux/macOS `python3`.

## Fluxo

### 1. Entender a ideia → spec
- Fonte: mensagem do usuário ou arquivo indicado (leia-o inteiro).
- Preencha mentalmente (ou num arquivo temporário fora do repo) `templates/spec.md`: objetivos, contrato público, restrições, matriz cenário → teste → pontos, starter, gabarito.
- Infira o que faltar com defaults sensatos (stack mais provável pelo contexto, tipo `implement`, CI GitHub, idioma do usuário). Pergunte **só** se faltar algo que muda o repo inteiro e não dá para inferir (ex.: linguagem totalmente ambígua). Liste suposições no resumo final.
- Destino: pasta indicada pelo usuário; senão `./exercicio-<slug>` no diretório atual. Não sobrescreva repo existente sem confirmação.

### 2. Escolher tipo e estratégias
Leia `exercise-types.md` e `assertion-strategies.md`. Defina para cada objetivo pelo menos uma estratégia verificável. Gradue a dificuldade (aquecimento/fácil/médio/difícil/🔥desafio) e os pontos (1/2/3).

### 3. Gerar a casca
```bash
python <SKILL_DIR>/scripts/scaffold.py --dest <pasta> --title "<Título>" --stack <perfil> --type <tipo> --ci github --git [--deadline "<prazo>"]
python <SKILL_DIR>/scripts/scaffold.py --list-stacks
```
Perfis: `java-maven`, `java-gradle`, `node`, `python`, `dotnet`, `go`, `rust`, `php`, `ruby`, `c-cpp`, `generic` (edite o setup do workflow à mão). `--ci gitlab|both|none` conforme a plataforma do usuário.

### 4. Escrever o projeto (gabarito primeiro)
Leia `references/stacks/<stack>.md`.
1. Crie o projeto base com o gerador oficial da stack quando existir (Spring Initializr, `npm init`, `dotnet new`, `go mod init`, `cargo new`) e inclua wrapper de build se a stack tiver.
2. Escreva a **solução completa** (gabarito).
3. Escreva os **testes** e as **fixtures** (request/response/datasets/features) cobrindo toda a matriz. Nomes de teste em linguagem do aluno.
4. Rode a suíte nativa até tudo passar.
5. Copie os arquivos da solução que o aluno deve escrever para uma pasta **fora do repo** (ex.: `<pasta>-gabarito/`, mesmos caminhos relativos) e substitua-os no repo pelo **starter**: mesma assinatura, `TODO` e retorno neutro que reprova (exceção "não implementado", `null`, status 500/501). Arquivos que não são objeto do exercício ficam completos.
   - Tipo `write-tests`: produção fica completa; os testes do autor viram o gabarito e saem do repo.
   - Tipo `fix-bug`: o gabarito é o código correto; o starter recebe os bugs plantados.

### 5. Escrever o README
Edite o README gerado (template do tipo): contexto narrativo, objetivo, ⚠️ atenção/restrições, modelo, funcionalidades numeradas com regras e exemplos (copie os JSONs das fixtures), tabela de erros, como rodar os testes, tabela de avaliação com pontos, como começar (fork/branch) e entregar, dicas que não entregam a solução. Remova todos os comentários `<!-- -->` e seções que não se aplicam. Escreva no idioma do usuário.

### 6. Pontuação e pipeline
Leia `grading-pipeline.md`. Substitua o teste TODO de `.github/classroom/autograding.json` por uma entrada por grupo da matriz, com `run` seletivo (seletor da stack), `points` e `timeout` (minutos). Proteja testes/fixtures/CI:
```bash
cd <pasta>
python .github/classroom/integrity.py --write <pasta-de-testes> <fixtures> .github/workflows .github/classroom/autograding.json
```
e acrescente ao autograding: `{"name": "0. Integridade dos arquivos protegidos", "setup": "", "run": "python3 .github/classroom/integrity.py --check || python .github/classroom/integrity.py --check", "input": "", "output": "", "comparison": "included", "timeout": 1, "points": 0, "required": true}`. Regere o manifesto sempre que alterar arquivo protegido (inclusive o autograding.json).

### 7. Verificar (obrigatório)
```bash
python .github/classroom/grade.py --validate
python <SKILL_DIR>/scripts/verify.py --repo <pasta> --solution <pasta>-gabarito
```
Critério: starter 0% (ou `--starter-max` para aquecimento declarado), gabarito 100%. Corrija e repita até `RESULTADO: OK`. Depois revise `authoring-checklist.md`. Se a toolchain da stack não estiver instalada localmente, diga isso claramente, rode ao menos `--validate`, e deixe a verificação para o CI.

### 8. Finalizar
- `git add` explícito dos arquivos do exercício + commit local `Initial commit` na branch `main` (repo novo, sem remoto). Push, criação de repositório remoto ou marcação como template só se o usuário pedir.
- Gabarito: por padrão fica na pasta externa e o usuário decide. Se pedirem, crie branch `solucao` com ele (nunca na `main`).
- Apague arquivos temporários (spec, relatórios, `grading-*.json|xml`).
- Resumo final curto: caminho do repo, tipo/stack, nº de testes e pontos, como o aluno começa (`fork` ou `git checkout -b resolucao/<nome>`), como rodar a nota local, resultado do verify, suposições feitas e onde está o gabarito.

## Regras
- O README é o único lugar com instruções; tudo que for testado tem que estar descrito nele (exceto bugs do fix-bug).
- Testes determinísticos: nada de data atual fixa em fixture (use datas distantes como 2099 ou calcule no teste), rede externa, porta fixa ou ordem implícita.
- Fixe versões de dependências; prefira libs de teste populares e mantidas.
- Não inclua segredos reais; use placeholders em `.env.example`.
- Mantenha o formato `.github/classroom/autograding.json` mesmo fora do GitHub (o runner e o Classroom o entendem).
