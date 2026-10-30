# Assertions

Contents:
- Two Accepted Libraries
- AssertJ — Preferred for New Tests
- JUnit Assertions — Accepted for Existing Tests
- Dual Verification — State + Behavior
- MockMvc Assertions — Controller Tests
- What Not to Use

## Two Accepted Libraries

Both are available via `spring-boot-starter-test`. Use AssertJ for new tests; JUnit Assertions are accepted when editing existing tests that already use them.

| Library | Import | When to use |
|---|---|---|
| AssertJ | `import static org.assertj.core.api.Assertions.*` | New tests — preferred |
| JUnit Assertions | `import static org.junit.jupiter.api.Assertions.*` | Existing tests — compatibility |

Do **not** mix both styles in the same test method.

---

## AssertJ — Preferred for New Tests

### Null checks

```java
assertThat(result).isNotNull();
assertThat(result).isNull();
```

### Equality

```java
assertThat(result).isEqualTo(expected);
assertThat(result.name()).isEqualTo("Test User");
```

### Booleans

```java
assertThat(result.active()).isTrue();
assertThat(result.isEmpty()).isFalse();
```

### Collections

```java
assertThat(result).hasSize(2);
assertThat(result).isEmpty();
assertThat(result.getContent()).hasSize(2);
assertThat(result.getContent().get(0).title()).isEqualTo("Expected Title");
```

### Optional

```java
assertThat(result).isPresent();
assertThat(result).isNotPresent();
assertThat(result).contains(expectedValue);
```

### Exceptions

```java
assertThatThrownBy(() -> useCase.getById(id))
    .isInstanceOf(AppException.class);
```

---

## JUnit Assertions — Accepted for Existing Tests

### Null checks

```java
assertNotNull(result);
assertNull(result);
```

### Equality

```java
assertEquals("Test User", result.name());
assertEquals(2, result.size());
assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
```

### Booleans

```java
assertTrue(result.isPresent());
assertFalse(result.isEmpty());
```

### Exceptions

```java
assertThrows(AppException.class, () -> useCase.getById(id));
assertDoesNotThrow(() -> useCase.delete(id));
```

Capture the exception to assert on its fields:

```java
AppException ex = assertThrows(AppException.class, () -> useCase.create(request));
assertEquals(Error.AUTOMATION_FLOW_NAME_ALREADY_EXISTS, ex.getError());
```

### Object identity

```java
assertSame(entity, saved);
```

---

## Dual Verification — State + Behavior

Every test must verify both what was **returned** and how **mocks were called**.

State is what came back; behavior is how dependencies were used.

```java
assertThat(result).isNotNull();
assertThat(result.name()).isEqualTo("Test User");

verify(persistencePort, times(1)).create(any(UserEntity.class));
verify(projectUserPort, never()).findAllByProjectId(any());
```

Never assert only state without verifying relevant mock interactions, and never verify mocks without asserting the return value (unless the method is void).

---

## MockMvc Assertions — Controller Tests

Used in `*APIControllerTest` classes. Chain `.andExpect()` calls after `.perform()`.

```java
mockMvc.perform(post("/api/v1/user")
        .contentType(MediaType.APPLICATION_JSON)
        .content(objectMapper.writeValueAsString(request)))
    .andExpect(status().isCreated())
    .andExpect(jsonPath("$.name").value("Test User"))
    .andExpect(jsonPath("$.email").value("test@example.com"));

mockMvc.perform(get("/api/v1/user/{id}", userId))
    .andExpect(status().isOk())
    .andExpect(content().contentType(MediaType.APPLICATION_JSON))
    .andExpect(jsonPath("$.content.length()").value(2));

mockMvc.perform(delete("/api/v1/user/{id}", userId))
    .andExpect(status().isNoContent());

mockMvc.perform(get("/api/v1/user/{id}", unknownId))
    .andExpect(status().isNotFound());
```

---

## What Not to Use

- **`assertAll`** — not used in this project; avoid introducing it
- **Soft assertions** (`SoftAssertions`) — not used; avoid introducing it
- **Hamcrest matchers** (`hasSize`, `is`, `equalTo`) — available but not the project standard; use AssertJ or JUnit Assertions instead
