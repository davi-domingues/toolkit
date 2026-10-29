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
    
    // Other mocked ports/mappers as needed
    
    @InjectMocks
    private <Domain>UseCaseImpl useCase;
    
    @BeforeEach
    void setUp() {
        // Initialize common fixtures, reusable entities
    }
    
    @Test
    void givenValidInput_whenAction_thenExpectedResult() {
        // Arrange
        // when(persistencePort.find(...)).thenReturn(...);
        
        // Act
        // ResultType result = useCase.action(...);
        
        // Assert
        // Assert state (result values)
        // verify(persistencePort).find(...) (Verify behavior)
    }
    
    @Test
    void givenInvalidCondition_whenAction_thenThrowException() {
        // Arrange
        // doThrow(...).when(persistencePort).action(...);
        
        // Act & Assert
        // assertThrows(AppException.class, () -> useCase.action(...));
        // verify(port).action(...)
        // verify(otherPort, never()).action(...)
    }
}
```