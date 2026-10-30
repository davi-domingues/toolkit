# Commit Message Template

## Title

- Repo with tickets: `<tipo>(<XX-NN>): <descricao curta>`
- Repo without tickets: `<tipo>: <descricao curta>`
- Maximum 72 characters for the full title.

Rules:
- `tipo`: Conventional Commits type in English: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `build`, `ci`, `style`.
- `XX-NN`: ticket key from the branch `<tipo>/<XX-NN>_<slug>`, matching `[A-Z]+-\d+` (e.g. `SA-156`). The branch type is open (feature, bugfix, refactor, hotfix, ...). Never invented: if not inferable, ask (see `references/checks-and-errors.md`).
- Text in pt-BR, plain ASCII: no accents, only simple alphanumeric characters and basic punctuation.
- Description short, in the third person, present indicative (`remove`, `adiciona`, `corrige`); not imperative (`remova`) nor past (`removido`). Must fit "Se aplicado, este commit: <titulo>".

## Body

Executive summary in one to three short sentences, then bullets with the macro changes (pt-BR, ASCII):

```
<tipo>(<XX-NN>): <descricao curta>

<resumo executivo>
- <mudanca 1>
- <mudanca 2>
```

## Examples

With ticket:
```
fix(SA-156): remove claim model do JWE

Remove a claim model do token para evitar vazamento de dados do modelo.
- remove a claim do gerador de JWE
- ajusta teste unitario do token
```

```
test(SA-156): cobre token sem cabecalho de autenticacao

Garante o comportamento quando o cabecalho de autenticacao esta ausente.
- adiciona teste para cabecalho ausente
```

Without ticket:
```
feat: adiciona skill readme-refresh

Adiciona ao toolkit a skill que reescreve o README a partir do codigo.
- adiciona SKILL.md e references da skill
- adiciona evals da skill
```

## Output formats

Proposal (mode a, mode c, or any proposal): one text block per commit with title and body, and nothing else. In mode a, also list the files of the commit before the approval request.

```
feat(SA-156): adiciona estrutura inicial de skills

Cria a base de skills e os indices do projeto.
- adiciona esqueleto das skills
- adiciona specs e indices iniciais
```

Execution (modes a and b): one line per commit, short hash and title, nothing else.

```
a1b2c3d feat(SA-156): adiciona estrutura inicial de skills
```
