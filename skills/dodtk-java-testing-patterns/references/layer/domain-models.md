# Domain Models Testing Rules

**Location:** `src/test/java/.../domain/model/`

Domain models in this project are primarily implemented as Java `record`s. They represent the core data structures with minimal logic.

## Core Principles
1. **Direct Instantiation**: Instantiate the records or domain classes directly via `new`.
2. **No Frameworks Required**: Pure JUnit 5 tests. No Mockito.

## Rules & Restrictions
- **Verify Equals and HashCode**: Since records automatically provide `equals` and `hashCode`, write a test validating identity comparison to document the contract.
- **Verify Accessors**: Assert that getter methods (or record accessor methods) return the exact data passed into the constructor.
- **Custom Logic Validation**: If the record has custom methods, constructors, or validation logic (e.g., throwing an error if a value is negative), test those branches exhaustively.

## Generic Skeleton

```java
class <Domain>ModelTest {

    @Test
    void givenSameFields_whenCompare_thenBeEqual() {
        UUID id = UUID.randomUUID();
        Model model1 = new Model(id, "Value");
        Model model2 = new Model(id, "Value");

        assertEquals(model1, model2);
        assertEquals(model1.hashCode(), model2.hashCode());
    }

    @Test
    void givenModel_whenAccessFields_thenReturnCorrectValues() {
        UUID id = UUID.randomUUID();
        Model model = new Model(id, "Value");

        assertEquals(id, model.id());
        assertEquals("Value", model.valueField());
    }

    @Test
    void givenInvalidData_whenConstruct_thenThrowException() {
        assertThrows(IllegalArgumentException.class, () -> new Model(null, "Value"));
    }
}
```

Include the third test only when the record has a compact constructor with validation.