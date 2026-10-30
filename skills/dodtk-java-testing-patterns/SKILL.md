---
name: dodtk-java-testing-patterns
description: The definitive testing standard for this project. Trigger this skill EVERY TIME the user asks to write, create, edit, fix, or organize unit tests. Whether the request is 'write a test', 'create tests', 'fix test', or 'unit test this class', it is required for ALL test creation and modification in the project. It guarantees that new unit tests follow the project's established mock structures, assertions, and layer-specific rules. It never modifies production code, project configurations, or any non-test files.
---

# Java Testing Patterns

Expert guide for writing unit tests in this project. All tests are pure unit tests — no Spring context is loaded.

## Required Context

Before writing, gather:

1. The class under test and its layer (Use Case, Persistence Adapter, Controller, Mapper, Domain Model, Infrastructure).
2. The nearest existing test class in the same repo, to copy its conventions.
3. The test dependencies declared in the repo's `build.gradle`.

If the class, the expected behavior or the layer is unclear, ask before writing.

## Filosofia de testes (agnostica de stack)

Princípios válidos em qualquer linguagem ou ferramenta de teste:

- Um conceito por teste.
- Verifique o estado (retorno) e o comportamento (interações com dependências).
- Estruture em preparar, agir e verificar, separados por linha em branco.
- Ordene: caminho feliz, depois alternativos, depois erros.
- Stubbing mínimo: configure só o que o teste usa.
- Fixture compartilhada só no setup; fábrica só quando a mesma construção se repete em vários testes.
- O nome descreve contexto, ação e resultado.
- Teste unitário é puro: sem subir contexto ou framework.
- Use só dependências já declaradas no projeto.
- Nunca altere código de produção para fazer o teste passar.
- Teste sem comentário. Única exceção ponderada: marcadores de preparar/agir/verificar quando a separação melhora a leitura.

## Constraints

- **Only use dependencies already declared** in `build.gradle` (JUnit 5, Mockito 5, AssertJ, MockMvc)
- **Never modify** production code, `build.gradle`, `application*.yaml`, or any file outside `src/test/`
- **Only allowed actions:** create tests, edit tests, organize directories under `src/test/java`
- When in doubt, **follow the existing test pattern** in the nearest similar test class

## Stack

| Tool | Role |
|---|---|
| JUnit 5 (Jupiter) | Test framework — `@Test`, `@BeforeEach`, `@ExtendWith` |
| Mockito 5 + mockito-inline | Mocking — `@Mock`, `@InjectMocks`, `MockedStatic` |
| AssertJ | Preferred assertions for new tests |
| JUnit Assertions | Accepted for compatibility with existing tests |
| MockMvc (standalone) | Controller HTTP testing — no Spring context |

## Core Rules

1. One concept per test method
2. Always verify both **state** (return value) and **behavior** (mock interactions via `verify`)
3. Structure every test as Arrange → Act → Assert, separated by blank lines. The `// Arrange` / `// Act` / `// Assert` markers are an exception: use them only when the three phases are distinct and the markers improve readability (long setup, several interactions, several asserts). In short or obvious tests, omit them. Never add any other comment in tests
4. Order tests: happy path first, then alternatives, then errors/exceptions
5. Avoid unnecessary stubbing — only configure what the specific test needs
6. Extract shared fixtures to `@BeforeEach setUp()`; test-specific setup stays inside the test, in its arrange phase
7. Use private factory methods for complex entities reused across multiple tests

## Quick Decision Tree (High-Level)

- **Need to know the architectural rules for a class?** → Read `references/testing-by-layer.md`
- **Need to structure the test class and setups?** → Read `references/test-structure.md`
- **Need to name test methods properly?** → Read `references/naming-conventions.md`
- **Need to mock dependencies, capture arguments, or mock statics?** → Read `references/mocking-patterns.md`
- **Need to make assertions and verify behaviors?** → Read `references/assertions.md`
- **Need to test multiple inputs for the same logic (parameterized tests)?** → Read `references/parameterized-tests.md`

## Step-by-Step Workflow

Follow these steps when creating or modifying a test from scratch:

**Step 1: Identify the Layer**
Always start by determining the layer of the class being tested (Use Case, Controller, Adapter, Mapper, or Domain). Read [references/testing-by-layer.md](references/testing-by-layer.md) to apply the mandatory architectural rules and limitations for that specific layer.

**Step 2: Setup the Structure**
Prepare the test skeleton, annotations, and `@BeforeEach` setup. Read [references/test-structure.md](references/test-structure.md) for the AAA (Arrange-Act-Assert) structure, when to use its markers, and fixture management, and [references/mocking-patterns.md](references/mocking-patterns.md) if you need Mockito setup.

**Step 3: Define the Test Names**
Before writing the test body, decide what behaviors you are testing and name them properly. Read [references/naming-conventions.md](references/naming-conventions.md) to choose the correct convention (prefer Given-When-Then).

**Step 4: Implement and Verify**
Write the test logic. Ensure you verify both the expected output (state) and the interaction with mocks (behavior). Read [references/assertions.md](references/assertions.md) for assertion rules.

**Step 5: Review Core Rules**
- Verify if constraints and core rules were followed properly
- Verify that `// Arrange` / `// Act` / `// Assert` markers appear only in tests where they help readability, and that no other comments were added

**Step 6: Run and Report**
Run the tests of the touched class with the repo's wrapper (`.\gradlew.bat test --tests <Class>` on Windows; the CI uses `./gradlew test jacocoTestReport`) and report the result.

## Definition of Done

- Tests created or edited only under `src/test/`.
- Every test verifies state and behavior, with one concept each.
- Names follow `references/naming-conventions.md`; no comments other than the optional phase markers.
- No unnecessary stubbing, no `@SpringBootTest`/`@WebMvcTest`/`@DataJpaTest`, no new dependency.
- Tests of the touched classes pass locally.

## Expected Output

Reply briefly, in these sections:

- **Criado/Alterado:** one line per test file, with the scenarios covered.
- **Verificação:** Gradle command run and result (passed/failed counts).
- **Pendências:** scenarios not covered, production behavior that looks wrong (reported, never fixed here) and questions for the user.

## Known Pitfalls

- `UnnecessaryStubbingException`: remove the unused stub or move it per `references/mocking-patterns.md`.
- `MockedStatic` not closed in `@AfterEach` leaks state between tests.
- A controller test with `Pageable` needs `PageableHandlerMethodArgumentResolver` in `standaloneSetup`.
- A failing test that points to a production bug: do not edit `src/main`; report it under **Pendências**.
