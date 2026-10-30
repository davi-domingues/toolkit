# Catálogo dos exemplos analisados

Origem: repos `2-SIS-2026-01/*` (template GitHub Classroom → cópia do aluno). Todos Java 21 + Spring Boot + H2 + Maven. Histórico típico: `Initial commit` → `add deadline` (bot) → commit(s) do aluno.

| Repo | Tipo | Domínio | Asserção | Seletor no autograding | Testes / pontos |
|------|------|---------|----------|------------------------|-----------------|
| atividade-01-sp-01 | katas | par, palíndromo, primo, Fibonacci via GET | MockMvc status + corpo exato (`@WebMvcTest`) | `-Dtest=Classe#metodo` (1 por caso) | 12 / 12 |
| atividade-spring-jdbc | implement | CRUD músicas + busca dinâmica (JdbcTemplate) | HTTP golden JSON + Database Rider (input/expected) + provider de inválidos | `-Dtest=MusicaTest$GetMusicas` (1 por endpoint) | 6 / 6 |
| exercicio-spring-jpa | implement | CRUD consoles + dynamic finders | idem JDBC | classe aninhada | 6 / 6 |
| exercicio-jdbc-clinica-medica | implement (+🔥 desafio) | pacientes, consultas, relatório por médico | golden JSON + datasets + regex de UUID | classe aninhada | 9 / 9 |
| exercicio-dto-bean-validation | implement | conta corrente, usuário, depósito | golden + datasets + ArchUnit + `ddl-auto=validate` | classe aninhada; arquitetura vale 3 | 6 / 8 |
| exercicio-many-to-one | implement | empresa → usuário → chamado, delete em cadeia via JPQL | golden + datasets + ArchUnit (4 regras separadas) | classe aninhada + método ArchUnit | 21 / 21 |
| exercicio-many-to-one-eventos | implement | eventos, inscrições, lotação, soft delete, resumo | RestTemplate + DBRider YAML + asserts de substring | `-Dtest=Classe#metodo` (1 por cenário) | 44 / 61 (1–2 pts) |
| exercicio-se-vira | fix-bug | kanban de tarefas | Cucumber pt-BR + MockMvc, tags por cenário | `-Dcucumber.filter.tags="@tag"` | 21 / 40 (1–3 pts) |
| exercicio-testes-unitarios-spring | write-tests | biblioteca (empréstimos) | JaCoCo BRANCH no pacote service, 10 execuções `check@check-coverage-N` | degraus 10…100% | 10 / 10 |
| exercicio-testes-unitarios-spring-2 | write-tests | hotel (reservas, check-in/out) | JaCoCo com profiles `-Pcoverage-N` + property `jacoco.coverage.minimum` | degraus 10…100% | 10 / 10 |
| projeto-individual-sprint-1 | project | tema livre, front vanilla + back JDBC/MySQL | sem autograding (avaliação manual) | — | — |

Repos de referência sem padrão de exercício (ignorados como modelo, úteis como conteúdo): `spring-security-jwt-exemplo` (exemplo didático com branches por versão), pastas sem `.git` (`api-*`, `ac02-many-to-one`, `bora-praticar-testes`).

## Lições extraídas
- **Unidade de nota = grupo de testes**, selecionado no comando. A ferramenta de teste não precisa conhecer pontos.
- **Fixtures separadas** tornam o README e os testes consistentes (mesmos JSONs).
- **Arquitetura como teste** transforma "boas práticas" em requisito verificável.
- **Degraus** (cobertura) dão nota parcial a meta-asserções que seriam binárias.
- **BDD com tags** serve de especificação legível quando o README é vago (fix-bug).
- **Dificuldade explícita** (👶 ⚖️ 💪 🔥, `[3pts]`) orienta o esforço do aluno.
