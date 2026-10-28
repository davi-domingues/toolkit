# Test Structure

## Standard Class Skeleton

```java
@ExtendWith(MockitoExtension.class)
class UserUseCaseImplTest {

    // Dependencies — one @Mock per port/dependency
    @Mock
    private UserPersistencePort userPersistencePort;

    @Mock
    private ProjectUserPort projectUserPort;

    // Class under test
    @InjectMocks
    private UserUseCaseImpl useCase;

    // Shared fixtures — initialized in setUp()
    private UUID userId;
    private UserEntity userEntity;

    @BeforeEach
    void setUp() {
        userId = UUID.randomUUID();
        userEntity = new UserEntity();
        userEntity.setId(userId);
        userEntity.setName("Test User");
        userEntity.setEmail("test@example.com");
    }

    @Test
    void givenExistingUser_whenGetById_thenReturnUser() {
        // Arrange
        when(userPersistencePort.getUserById(userId)).thenReturn(userEntity);

        // Act
        User result = useCase.getUserById(userId);

        // Assert
        assertNotNull(result);
        assertEquals("Test User", result.name());
        verify(userPersistencePort).getUserById(userId);
    }

    @Test
    void givenNonExistentUser_whenGetById_thenThrowException() {
        // Arrange
        when(userPersistencePort.getUserById(userId)).thenThrow(new AppException(Error.USER_NOT_FOUND));

        // Assert + Act
        assertThrows(AppException.class, () -> useCase.getUserById(userId));
        verify(userPersistencePort).getUserById(userId);
    }
}
```

## AAA Pattern

Every test must follow Arrange-Act-Assert with explicit comments:

```java
// Arrange  — set up mocks and inputs
// Act      — call the method under test (single call)
// Assert   — verify return value AND mock interactions
```

When the assertion is `assertThrows`, combine Act and Assert:

```java
// Arrange
when(port.findById(id)).thenReturn(Optional.empty());

// Act + Assert
AppException ex = assertThrows(AppException.class, () -> useCase.getById(id));
assertEquals(Error.NOT_FOUND, ex.getError());
verify(port).findById(id);
verify(port, never()).save(any());
```

## Test Ordering Within a Class

Order test methods to tell a story:

1. **Happy path** — the main successful scenario
2. **Alternative paths** — valid but non-default scenarios
3. **Error/exception paths** — invalid inputs, not-found, conflicts

```java
// 1. Happy path
void givenValidRequest_whenCreate_thenReturnCreated() { }

// 2. Alternative
void givenExistingUser_whenCreateOrFind_thenReturnExisting() { }

// 3. Errors
void givenDuplicateName_whenCreate_thenThrowException() { }
void givenNonExistentId_whenGetById_thenThrowException() { }
```

## `@BeforeEach` — What Goes Here

Put in `setUp()` only what is **shared across multiple tests** in the class:

```java
@BeforeEach
void setUp() {
    // IDs
    projectId = UUID.randomUUID();

    // Entities with common state
    projectEntity = new ProjectEntity();
    projectEntity.setId(projectId);
    projectEntity.setName("Test Project");

    // Expected responses
    projectResponse = new ProjectResponse(projectId, "Test Project");
}
```

Test-specific setup stays inside the test's `// Arrange` block — do not pollute `setUp()` with it.

## Private Factory Methods

Use when the same complex entity is constructed in 3 or more tests:

```java
private AutomationFlowEntity createFlowEntity(UUID id, String name, UserEntity creator) {
    return AutomationFlowEntity.builder()
            .id(id)
            .name(name)
            .creator(creator)
            .downloadCount(0)
            .createdAt(LocalDateTime.now())
            .build();
}

private UserEntity createUserEntity(UUID id, String name) {
    UserEntity user = new UserEntity();
    user.setId(id);
    user.setName(name);
    return user;
}
```

Do **not** create factory methods for entities used in only one or two tests — inline them in `// Arrange`.

## `@AfterEach` — When to Use

Only required when using `MockedStatic`. Always close it to release the static mock:

```java
private MockedStatic<SpringApplication> springApplicationMock;

@BeforeEach
void setUp() {
    springApplicationMock = mockStatic(SpringApplication.class);
}

@AfterEach
void tearDown() {
    springApplicationMock.close(); // mandatory — prevents state leaking between tests
}
```
