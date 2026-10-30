# Estratégias de asserção

Catálogo de "métodos de asserção" observados nos repos de treino, generalizados. Combine vários por exercício. Para ferramentas concretas por linguagem, abra `stacks/<stack>.md`.

Regra de ouro: **teste o contrato observável, não a implementação** — exceto quando a implementação é o objetivo (arquitetura, uso de uma API específica), e então teste isso explicitamente com uma regra própria.

## 1. Saída exata / I/O
Entrada → saída de uma função, endpoint ou programa.
- Katas, funções puras, CLIs (stdin → stdout).
- Sem framework: `autograding.json` com `input` + `output` + `comparison` (`exact`/`included`/`regex`) já resolve (ex.: `"run": "python main.py", "input": "5\n", "output": "120"`).
- Inclua bordas: zero, negativo, vazio, nulo, unicode/maiúsculas, valor grande, limite exato.

## 2. Contrato HTTP com golden files
Requisição real à aplicação rodando em memória/porta aleatória; status + corpo comparados com JSON esperado.
- Fixtures: `request/<caso>.json`, `response/<caso>.json`. Compare como **árvore JSON** (ordem de chaves irrelevante), não como string.
- Campos não determinísticos (UUID, datas, timestamps): substitua por regex antes de comparar, ou injete relógio/gerador fixo, ou compare só presença/formato.
- Cubra todos os status do contrato: 200/201/204/400/404/409/422.

## 3. Estado persistido (datasets antes/depois)
Carrega um dataset inicial no banco, executa a operação, compara o banco com o dataset esperado.
- Layout: `datasets/input/<cenário>.(json|yml|sql)`, `datasets/expected/<cenário>.*`.
- Pegue efeitos colaterais que a resposta não mostra: delete em cascata, soft delete (`cancelada=true`), update que não pode alterar o ID, operação inválida que **não** pode alterar o banco (expected = input).
- Reinicie sequências/IDs para resultados previsíveis (`ALTER ... RESTART WITH n`). Limpe o banco antes/depois de cada teste.
- Comparação `CONTAINS` quando o teste só se importa com a linha nova.

## 4. Validação de entrada parametrizada
Um teste parametrizado, N arquivos/linhas de entrada inválida, mesmo resultado esperado.
- Um caso por regra: ausente, nulo, vazio, só espaços, formato inválido, abaixo do mínimo, acima do máximo, tipo errado, duplicado.
- Nome do caso legível ("Deve retornar 400 quando duração for zero") — vira a mensagem que o aluno lê.

## 5. Regras de negócio / cenários de erro
Conflitos e fluxos: lotação máxima, duplicidade (409), recurso inexistente (404), estado inválido (ex.: devolver algo já devolvido), data no passado, cálculo agregado (média, contagem, vagas restantes).
- Um teste por regra; regras derivadas ("não armazenar campo calculado") testadas pelo efeito (comportamento após mudar dados).

## 6. Arquitetura / estrutura
Regras de dependência entre camadas, nomes, pastas.
- "controller não acessa repository/entity", "service não depende de controller nem de outro service", "DTO não depende de entity".
- Ferramentas: ArchUnit (JVM), dependency-cruiser/eslint-plugin-boundaries (JS/TS), import-linter/pytest-archon (Python), NetArchTest (.NET), go-arch-lint ou teste com `go list -deps` (Go). Fallback universal: script que faz grep de imports proibidos.
- Pode valer mais pontos (3) por exigir refatoração global.

## 7. Esquema / configuração
O mapeamento declarado bate com o esquema real (ex.: ORM `ddl-auto=validate`, migrations aplicam do zero, `tsc --noEmit`, `terraform validate`, `docker compose config`).

## 8. Comportamento em linguagem natural (BDD)
Gherkin (`Dado/Quando/Então`, `# language: pt`) com tags por cenário (`@cadastrar-duplicado`).
- Ideal para fix-bug e para alunos lerem a especificação como documentação.
- Cada tag = 1 entrada no autograding. Steps reutilizáveis, contexto compartilhado entre steps, limpeza do estado em hook `Before`.
- Ferramentas: Cucumber (JVM/JS), behave/pytest-bdd (Python), Reqnroll/SpecFlow (.NET), godog (Go).

## 9. Cobertura em degraus (meta-asserção para write-tests)
Roda os testes do aluno e checa cobertura mínima no pacote alvo: 10%, 20%, … 100%, 1 ponto cada.
- Prefira cobertura de **branches** no módulo de regras de negócio, não do projeto inteiro.
- Rode a suíte 1x no `setup` da primeira entrada; as demais só checam o relatório.
- Combine com: testes do aluno precisam **passar** (degrau 0), integridade de `src/main`, e opcionalmente **mutation testing** (PIT, Stryker, mutmut, Stryker.NET, go-mutesting) para impedir testes sem assert.

## 10. Testes do aluno contra implementações quebradas (mutantes manuais)
Alternativa leve ao mutation testing: o autor guarda K versões defeituosas do código de produção; cada degrau troca a produção pela versão defeituosa e espera que a suíte do aluno **falhe**. Cada mutante detectado = 1 ponto.

## 11. Integridade (gate)
O aluno não pode alterar testes, fixtures, CI ou (no write-tests) produção.
- `scripts/integrity.py --write <caminhos>` gera `.github/classroom/protected.sha256`; no autograding uma entrada `"run": "python3 .github/classroom/integrity.py --check || python .github/classroom/integrity.py --check", "points": 0, "required": true` zera a nota se algo mudou (o fallback `python` cobre Windows, onde `python3` costuma ser só o atalho da Store).
- Alternativa: `git diff --exit-code <sha-do-template> -- <caminhos>` (exige histórico completo no checkout: `fetch-depth: 0`).

## 12. Estático / estilo / restrições de dependência
Lint sem erros, formatação, proibição de libs ("não use frameworks no front"), manifesto sem dependências novas.
- Implemente como script que lê o manifesto (`package.json`, `pom.xml`, `requirements.txt`) ou o HTML/imports e falha se encontrar algo proibido. Saída clara do que foi encontrado.

## 13. UI / end-to-end
Navegador headless (Playwright/Cypress/Selenium) contra a página servida localmente: campos obrigatórios existem (por `id`/`name`/`data-testid` definidos no README), validação no cliente bloqueia envio inválido, dropdown carregado via API (mock de rede).
- Defina os seletores no README — eles são parte do contrato.

## 14. Desempenho / complexidade
Limite de tempo com entrada grande (ex.: Fibonacci n=90 em < 1s) usando `timeout` da entrada ou do framework. Use folga generosa (CI é mais lento que máquina local).

## Escolhendo
| Objetivo de aprendizagem | Estratégias |
|--------------------------|-------------|
| Lógica/algoritmo | 1, 14 |
| API REST / CRUD | 2, 3, 4, 5 |
| Modelagem/ORM/relacionamentos | 3, 7, 5 |
| Arquitetura em camadas, DTOs | 6, 2 |
| Testes unitários | 9, 10, 11 |
| Depuração | 8 (ou 2/3), 11 |
| Front-end | 13, 12 |
| Projeto integrado | 2, 12, 13 + rubrica |
