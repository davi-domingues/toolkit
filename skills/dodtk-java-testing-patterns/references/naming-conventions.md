# Naming Conventions

## Class Names

Suffix the tested class with `Test`. Mirror the production package under `src/test/java`.

```
UserUseCaseImpl           → UserUseCaseImplTest
UserAPIController         → UserAPIControllerTest
UserPersistenceAdapter    → UserPersistenceAdapterTest
ProjectMapper             → ProjectMapperTest
```

## Method Names

### Primary — Given-When-Then camelCase

Use when the test has a meaningful precondition worth naming.

```java
@Test
void givenExistingUser_whenGetById_thenReturnUser() { }

@Test
void givenDuplicateName_whenCreate_thenThrowException() { }

@Test
void givenEmptyRepository_whenFindAll_thenReturnEmptyList() { }
```

### Alternative 1 — `should*` camelCase

Use when the precondition is obvious from `@BeforeEach` setup and doesn't need naming.

```java
@Test
void shouldCreateAutomationFlowSuccessfully() { }

@Test
void shouldThrowExceptionWhenFlowNotFound() { }

@Test
void shouldReturnEmptyOptionalWhenNotFound() { }
```

### Alternative 2 — `context_WhenCondition_ShouldBehavior`

Use for adapter/repository tests with multiple scenarios on the same method.

```java
@Test
void findAll_WhenEntitiesExist_ShouldReturnMappedResponses() { }

@Test
void findAll_WhenNoEntitiesExist_ShouldReturnEmptyList() { }

@Test
void save_WhenEntityIsValid_ShouldPersistAndReturn() { }
```

### Alternative 3 — `test*` (legacy only)

Do **not** use in new tests. Acceptable only for maintenance of existing tests that already follow this style.

```java
void testCreateUser() { }
void testGetUserById_UserFound() { }
```

## Choosing the Right Style

| Situation | Use |
|---|---|
| New test, meaningful precondition | GWT camelCase |
| New test, precondition clear from `@BeforeEach` | `should*` |
| Adapter/repository with many scenarios per method | `context_When_Should` |
| Editing an existing `test*` method | Keep `test*` for consistency |

## `@DisplayName`

Use `@DisplayName` on the **class** when the suite has more than 10 tests, to improve test report readability.

```java
@ExtendWith(MockitoExtension.class)
@DisplayName("AutomationFlowUseCaseImpl — Unit Tests")
class AutomationFlowUseCaseImplTest { }
```

Use `@DisplayName` on **methods** only for complex scenarios where the method name alone is insufficient.

```java
@Test
@DisplayName("Should set creator, provider and initial download count to zero on creation")
void givenValidRequest_whenCreate_thenSetInitialValues() { }
```
