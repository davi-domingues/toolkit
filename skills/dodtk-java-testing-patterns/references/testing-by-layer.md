# Testing by Layer

This project follows Hexagonal Architecture. Each layer has a distinct testing pattern.

Identify the layer of the class you are testing and read the corresponding reference.

## Quick Decision Tree: Layer Selection

```
Writing a test for...

  A Use Case (business logic)?
    → Plain JUnit + @Mock/@InjectMocks
    → See: layer/use-cases.md

  A Persistence Adapter?
    → Plain JUnit + @Mock/@InjectMocks (mock the repository)
    → See: layer/persistence-adapters.md

  A Controller (HTTP behavior)?
    → MockMvcBuilders.standaloneSetup() — no @WebMvcTest
    → See: layer/controllers.md

  A MapStruct Mapper?
    → Real instance via Mapper.INSTANCE — no mocks
    → See: layer/mappers.md

  A Domain Model (Record)?
    → Direct instantiation — no mocks
    → See: layer/domain-models.md
    
  Infrastructure or Config?
    → Direct instantiation — no Spring context
    → See: layer/infrastructure.md
```

The skeletons in `layer/*.md` are comment-free; names between `<...>` are placeholders to replace with the real types. The `// Arrange` / `// Act` / `// Assert` markers follow the criterion in [test-structure.md](test-structure.md).

## At a Glance

| Layer | Spring context? | Mocking strategy | Assertion style |
|---|---|---|---|
| Use Cases | No | `@Mock` + `@InjectMocks` | JUnit / AssertJ + `verify` |
| Persistence Adapters | No | `@Mock` + `@InjectMocks` | JUnit / AssertJ + `verify` |
| Controllers | No | `mock()` in `@BeforeEach` + MockMvc standalone | `andExpect` + `jsonPath` |
| Mappers | No | No mocks — real `Mapper.INSTANCE` | JUnit / AssertJ |
| Domain Models | No | No mocks — direct instantiation | JUnit / AssertJ |
| Infrastructure | No | No mocks — direct instantiation | JUnit / AssertJ |
