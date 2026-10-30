# Tipos de exercício

Escolha um tipo (ou combine: ex. `implement` + desafio de arquitetura). O tipo define o template de README, o que vai no starter e como a nota é calculada.

## implement — construir a partir de um contrato
Mais comum (7 dos 11 repos analisados: CRUD JDBC, CRUD JPA, DTO+Bean Validation, Many-to-One, clínica médica, eventos).

- **Starter:** projeto completo e compilável; entidades/DTOs/serviços/controllers como esqueleto ou ausentes; config de banco/infra pronta.
- **Testes:** integração ponta a ponta do contrato público (HTTP, CLI, função pública), estado persistido, validações, regras de negócio, arquitetura.
- **README:** `templates/readme/implement.md`. Contrato completo com exemplos de request/response e tabela de erros.
- **Nota:** 1 entrada por funcionalidade (ou por cenário, se quiser granularidade fina). Desafios valem mais.
- **Use quando:** o objetivo é aprender a construir algo (API, lib, CLI, componente de UI, pipeline de dados, IaC).

## katas — vários exercícios curtos e independentes
Ex.: `atividade-01-sp-01` (par/ímpar, palíndromo, primo, Fibonacci como endpoints).

- **Starter:** uma função/arquivo por exercício com assinatura pronta e retorno neutro.
- **Testes:** casos de entrada → saída por exercício, incluindo bordas (0, negativo, maiúsculas, valores grandes).
- **README:** `templates/readme/katas.md` — "Exercício 0 (aquecimento) / 1 👶 / 2 ⚖️ / 3 💪", com "Cenários testados" numerados.
- **Nota:** 1 entrada por caso de teste (`Exercício 2 - Caso 3`). O aquecimento pode não valer ponto.
- **Use quando:** lógica, algoritmos, sintaxe de uma linguagem nova, regex, SQL queries, funções puras.

## write-tests — o aluno escreve os testes
Ex.: `exercicio-testes-unitarios-spring` (1 e 2): API pronta, aluno cria testes unitários com mocks; nota por degraus de cobertura.

- **Starter:** código de produção 100% pronto e correto. Pasta de testes vazia ou com 1 esqueleto de classe.
- **Asserção:** ferramenta de cobertura com limiares (10%, 20% … 100%), cada degrau = 1 entrada. Opcional e recomendado: mutation testing (cobertura sozinha é burlável com testes sem assert) e integridade de `src/main` (o aluno não pode mudar produção).
- **README:** `templates/readme/write-tests.md` — tabela de cenários obrigatórios por método, snippets de mock/assert/captor, critério de aprovação.
- **Nota:** degraus de cobertura (+ degraus de mutation score, se houver). Gate `required` de integridade.
- **Use quando:** ensinar testes unitários, mocks, TDD reverso, cobertura de branches.

## fix-bug — fazer funcionar
Ex.: `exercicio-se-vira`: "Se vira, faz funcionar e passar nos testes." Bugs plantados: anotação faltando, dependência ausente, generics invertidos, rota errada, método de query inválido, `server.port=-8080`, `ddl-auto=drop`.

- **Starter:** sistema quase pronto com N defeitos plantados em camadas diferentes (build, config, código, contrato). O README não lista os bugs.
- **Testes:** especificação de comportamento correto (BDD/Gherkin funciona bem: legível como documentação), agrupados por tags.
- **Plantar bugs (variar):** erro de compilação, config inválida, dependência faltando, rota/nome divergente, lógica off-by-one, tratamento de erro ausente (500 em vez de 404/409), validação faltando, query errada.
- **README:** `templates/readme/fix-bug.md` (curto e propositalmente vago).
- **Nota:** por cenário, 1–3 pontos conforme profundidade do bug.
- **Use quando:** depuração, leitura de código alheio, stack traces, configuração.

## project — projeto mais aberto com rubrica
Ex.: `projeto-individual-sprint-1`: tema livre, front vanilla + back Spring + MySQL; requisitos técnicos obrigatórios (tipos de input, dropdown via API, validação, 201/400).

- **Starter:** estrutura de pastas por camada (`frontend/`, `backend/`), configs e um README por parte. Pouco ou nenhum código de domínio.
- **Asserção:** automatizar só o objetivo e verificável (build passa, endpoints existem e retornam os status certos, ausência de libs proibidas via checagem estática do manifesto/HTML). O restante vai para `RUBRICA.md` (avaliação manual).
- **README:** `templates/readme/project.md` + `templates/RUBRICA.md`.
- **Use quando:** integração de várias camadas, tema escolhido pelo aluno, entrega de sprint.

## Matriz rápida

| Tipo | Aluno escreve | Testes fornecidos? | Unidade de nota | Template |
|------|---------------|--------------------|-----------------|----------|
| implement | produção | sim | funcionalidade/cenário | implement.md |
| katas | funções curtas | sim | caso de teste | katas.md |
| write-tests | testes | não (só meta-asserção) | degrau de cobertura/mutação | write-tests.md |
| fix-bug | correções | sim | cenário/tag | fix-bug.md |
| project | tudo | parcial | requisito objetivo + rubrica | project.md |
