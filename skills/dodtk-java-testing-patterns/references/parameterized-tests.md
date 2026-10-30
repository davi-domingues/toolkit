# Parameterized Tests

Contents:
- `@ValueSource`
- `@CsvSource`
- `@MethodSource`
- `@EnumSource`
- Naming Parameterized Tests
- When to Use vs. Separate Test Methods

Use `@ParameterizedTest` when the same behavior needs to be verified with multiple inputs. This avoids duplicating test methods that differ only in their data.

`junit-jupiter-params` is included transitively via `spring-boot-starter-test` — no additional dependency needed.

---

## `@ValueSource` — Simple literal values

Use for a single argument of a primitive or String type.

```java
@ParameterizedTest
@ValueSource(strings = {"", " ", "   "})
void givenBlankName_whenCreate_thenThrowException(String blankName) {
    PersonaRequest request = new PersonaRequest(blankName, "Description");

    assertThrows(AppException.class, () -> useCase.create(request));
}

@ParameterizedTest
@ValueSource(ints = {0, -1, -100})
void givenNonPositiveCount_whenValidate_thenReturnFalse(int count) {
    assertFalse(validator.isValid(count));
}
```

---

## `@CsvSource` — Multiple arguments inline

Use when the test needs two or more correlated inputs.

```java
@ParameterizedTest
@CsvSource({
    "DEV,  Developer",
    "QA,   Quality Assurance",
    "OPS,  Operations"
})
void givenRoleCode_whenGetDisplayName_thenReturnCorrectLabel(String code, String expectedLabel) {
    String result = roleUseCase.getDisplayName(code);

    assertEquals(expectedLabel, result);
}
```

---

## `@MethodSource` — Complex objects from a factory method

Use when inputs are objects that cannot be expressed as CSV literals.

```java
@ParameterizedTest
@MethodSource("invalidUserRequests")
void givenInvalidRequest_whenCreate_thenThrowException(UserRequest request) {
    assertThrows(AppException.class, () -> useCase.create(request));
}

static Stream<UserRequest> invalidUserRequests() {
    return Stream.of(
        new UserRequest(null, "email@test.com"),
        new UserRequest("", "email@test.com"),
        new UserRequest("Valid Name", null),
        new UserRequest("Valid Name", "not-an-email")
    );
}
```

---

## `@EnumSource` — Enum constants

Use to run a test against all or a subset of enum values.

All values:

```java
@ParameterizedTest
@EnumSource(EnumMood.class)
void givenAnyMood_whenCreatePersona_thenAccept(EnumMood mood) {
    PersonaRequest request = new PersonaRequest("Assistant", "Description", mood);
    assertDoesNotThrow(() -> useCase.create(request));
}
```

Subset of values:

```java
@ParameterizedTest
@EnumSource(value = EnumMood.class, names = {"HAPPY", "NEUTRAL"})
void givenPositiveMood_whenScore_thenReturnHighScore(EnumMood mood) {
    int score = scorer.score(mood);
    assertTrue(score >= 5);
}
```

---

## Naming Parameterized Tests

Use `@ParameterizedTest(name = "...")` with `{0}`, `{1}` placeholders to produce readable test names in reports.

```java
@ParameterizedTest(name = "blank name [{0}] should throw exception")
@ValueSource(strings = {"", " ", "   "})
void givenBlankName_whenCreate_thenThrowException(String blankName) { }

@ParameterizedTest(name = "role [{0}] should display as [{1}]")
@CsvSource({"DEV, Developer", "QA, Quality Assurance"})
void givenRoleCode_whenGetDisplayName_thenReturnLabel(String code, String label) { }
```

---

## When to Use vs. Separate Test Methods

| Situation | Use |
|---|---|
| Same logic, 3+ different inputs | `@ParameterizedTest` |
| Same logic, 2 inputs | Either — prefer separate methods if names add clarity |
| Different logic per scenario | Separate `@Test` methods |
| Inputs are complex objects with setup | `@MethodSource` |
| Inputs are simple literals | `@ValueSource` or `@CsvSource` |
