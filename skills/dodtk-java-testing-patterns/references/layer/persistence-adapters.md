# Persistence Adapters Testing Rules

**Location:** `src/test/java/.../adapter/out/persistence/adapter/`

Persistence Adapters implement the outgoing ports by mapping domain objects to JPA entities and delegating to Spring Data repositories.

## Core Principles
1. **Mock Repositories**: Use `@Mock` for the Spring Data `@Repository` interfaces. Do NOT load a real database or use `@DataJpaTest`.
2. **Mock Mappers**: Use `@Mock` for the MapStruct mappers used to convert between Domain and Entity.
3. **Focus on Mapping and Delegation**: The goal is to verify that the adapter calls the repository with the right entity and returns the right domain object.

## Rules & Restrictions
- **No Spring Context**: Do not use `@SpringBootTest` or `@DataJpaTest`.
- **Save Operations**: When testing a `save` or `create` method that returns the saved entity, mock the repository to return the argument passed to it using `thenAnswer(invocation -> invocation.getArgument(0))`.
- **Avoid JPA Logic**: Do not test cascade, lazy loading, or custom query syntax here (since the repository is mocked).

## Generic Skeleton

```java
@ExtendWith(MockitoExtension.class)
class <Domain>PersistenceAdapterTest {

    @Mock
    private <Domain>EntityRepository repository;

    @Mock
    private <Domain>Mapper mapper;

    @InjectMocks
    private <Domain>PersistenceAdapter adapter;

    @BeforeEach
    void setUp() {
        // Initialize shared entities and domain objects
    }

    @Test
    void givenValidDomain_whenSave_thenReturnSavedDomain() {
        // Arrange
        // Mock mapper to return Entity
        // Mock repository save with thenAnswer
        // Mock mapper to return Domain back
        
        // Act
        // Domain result = adapter.save(domain);
        
        // Assert
        // Verify state (result is mapped correctly)
        // Verify behavior: verify(repository).save(entity)
    }

    @Test
    void givenNonExistentId_whenFind_thenReturnEmptyOrThrow() {
        // Arrange
        // when(repository.findById(id)).thenReturn(Optional.empty());
        
        // Act & Assert
        // Verify it throws the expected exception or returns Optional.empty()
        // verify(mapper, never()).toModel(any()) -> important to verify mapper wasn't called
    }
}
```