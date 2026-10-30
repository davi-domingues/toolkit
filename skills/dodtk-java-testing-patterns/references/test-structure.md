# Test Structure

Contents:
- Standard Class Skeleton
- AAA Pattern and phase markers
- Test Ordering Within a Class
- `@BeforeEach` — What Goes Here
- Private Factory Methods
- `@AfterEach` — When to Use

## Standard Class Skeleton

```java
@ExtendWith(MockitoExtension.class)
class UserUseCaseImplTest {

    @Mock
    private UserPersistencePort userPersistencePort;

    @Mock
    private ProjectUserPort projectUserPort;

    @InjectMocks
    private UserUseCaseImpl useCase;

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
        when(userPersistencePort.getUserById(userId)).thenReturn(userEntity);

        User result = useCase.getUserById(userId);

        assertNotNull(result);
        assertEquals("Test User", result.name());
        verify(userPersistencePort).getUserById(userId);
    }

    @Test
    void givenNonExistentUser_whenGetById_thenThrowException() {
        when(userPersistencePort.getUserById(userId)).thenThrow(new AppException(Error.USER_NOT_FOUND));

        assertThrows(AppException.class, () -> useCase.getUserById(userId));
        verify(userPersistencePort).getUserById(userId);
    }
}
```

## AAA Pattern

Every test follows Arrange-Act-Assert as its mental structure, with the phases separated by blank lines:

- **Arrange** — set up mocks and inputs
- **Act** — call the method under test (single call)
- **Assert** — verify return value AND mock interactions

### Phase markers (`// Arrange`, `// Act`, `// Assert`)

The markers are an exception to the "no comments in code" rule and are **optional**. Use them only when both are true:

- the test has three clearly distinct phases; and
- the markers improve readability (long setup, several interactions, several asserts).

Do **not** use them in short or obvious tests (1-3 lines, no relevant setup, simple parameterized tests): the blank-line separation is enough. Never add any other comment to a test.

With markers (long setup, several interactions and asserts):

```java
@Test
void givenValidRequest_whenCreateProject_thenPersistAndNotifyMembers() {
    // Arrange
    ProjectRequest request = new ProjectRequest("Test Project", List.of(memberId, ownerId));
    when(userPersistencePort.getUserById(ownerId)).thenReturn(ownerEntity);
    when(userPersistencePort.getUserById(memberId)).thenReturn(memberEntity);
    when(projectPersistencePort.save(any())).thenAnswer(invocation -> invocation.getArgument(0));

    // Act
    Project result = useCase.create(request);

    // Assert
    assertNotNull(result);
    assertEquals("Test Project", result.name());
    assertEquals(2, result.members().size());
    verify(projectPersistencePort).save(any());
    verify(notificationPort, times(2)).notifyMember(any());
}
```

Without markers (short test):

```java
@Test
void givenExistingUser_whenGetById_thenReturnUser() {
    when(port.findById(id)).thenReturn(Optional.of(userEntity));

    User result = useCase.getById(id);

    assertEquals("Test User", result.name());
    verify(port).findById(id);
}
```

When the assertion is `assertThrows`, Act and Assert are combined in the same statement:

```java
when(port.findById(id)).thenReturn(Optional.empty());

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
void givenValidRequest_whenCreate_thenReturnCreated() { }

void givenExistingUser_whenCreateOrFind_thenReturnExisting() { }

void givenDuplicateName_whenCreate_thenThrowException() { }
void givenNonExistentId_whenGetById_thenThrowException() { }
```

## `@BeforeEach` — What Goes Here

Put in `setUp()` only what is **shared across multiple tests** in the class:

```java
@BeforeEach
void setUp() {
    projectId = UUID.randomUUID();

    projectEntity = new ProjectEntity();
    projectEntity.setId(projectId);
    projectEntity.setName("Test Project");

    projectResponse = new ProjectResponse(projectId, "Test Project");
}
```

Test-specific setup stays inside the test's arrange phase — do not pollute `setUp()` with it.

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

Do **not** create factory methods for entities used in only one or two tests — inline them in the test's arrange phase.

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
    springApplicationMock.close();
}
```
