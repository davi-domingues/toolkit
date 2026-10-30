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

    private <Domain> domain;
    private <Domain>Entity entity;

    @BeforeEach
    void setUp() {
        domain = new <Domain>(UUID.randomUUID(), "Value");
        entity = new <Domain>Entity();
    }

    @Test
    void givenValidDomain_whenSave_thenReturnSavedDomain() {
        when(mapper.toEntity(domain)).thenReturn(entity);
        when(repository.save(any(<Domain>Entity.class))).thenAnswer(invocation -> invocation.getArgument(0));
        when(mapper.toModel(entity)).thenReturn(domain);

        <Domain> result = adapter.save(domain);

        assertEquals(domain, result);
        verify(repository).save(entity);
    }

    @Test
    void givenNonExistentId_whenFind_thenReturnEmpty() {
        UUID id = UUID.randomUUID();
        when(repository.findById(id)).thenReturn(Optional.empty());

        Optional<<Domain>> result = adapter.findById(id);

        assertTrue(result.isEmpty());
        verify(mapper, never()).toModel(any());
    }
}
```

The `never()` verification on the mapper confirms it was not called when nothing was found. When the adapter throws instead of returning an empty `Optional`, replace the call and the `isEmpty()` assertion with `assertThrows` on the expected exception.