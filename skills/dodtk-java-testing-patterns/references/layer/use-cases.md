# Use Cases Testing Rules

**Location:** `src/test/java/.../domain/usecases/impl/`

Use Cases hold the core business logic. They orchestrate domain entities and delegate data operations to outgoing ports.

## Core Principles
1. **Mock all outgoing ports**: Use `@Mock` for persistence and external ports.
2. **Inject into Use Case**: Use `@InjectMocks` on the `*UseCaseImpl` class.
3. **Pure Unit Testing**: No Spring Boot annotations.
4. **Behavior Validation**: You MUST verify both the returned results AND the specific calls made to the ports.

## Rules & Restrictions
- **Do not** test the internal logic of mappers heavily here; focus on the business rules.
- **Do not** stub methods that won't be called.
- When an exception is expected, assert the specific custom exception type (e.g., `AppException`) and its specific error code.
- Always use `verify(port, never()).method()` for branches where a port should definitely not be invoked.

## Generic Skeleton

```java
@ExtendWith(MockitoExtension.class)
class <Domain>UseCaseImplTest {

    @Mock
    private <Domain>PersistencePort persistencePort;

    @Mock
    private <Other>Port otherPort;

    @InjectMocks
    private <Domain>UseCaseImpl useCase;

    private <Domain>Entity entity;

    @BeforeEach
    void setUp() {
        entity = new <Domain>Entity();
    }

    @Test
    void givenValidInput_whenAction_thenExpectedResult() {
        UUID id = UUID.randomUUID();
        when(persistencePort.find(id)).thenReturn(entity);

        ResultType result = useCase.action(id);

        assertNotNull(result);
        verify(persistencePort).find(id);
    }

    @Test
    void givenInvalidCondition_whenAction_thenThrowException() {
        UUID id = UUID.randomUUID();
        doThrow(new AppException(Error.<ERROR_CODE>)).when(persistencePort).action(id);

        AppException ex = assertThrows(AppException.class, () -> useCase.action(id));

        assertEquals(Error.<ERROR_CODE>, ex.getError());
        verify(persistencePort).action(id);
        verify(otherPort, never()).action(id);
    }
}
```

Add one `@Mock` per outgoing port or mapper the use case depends on.