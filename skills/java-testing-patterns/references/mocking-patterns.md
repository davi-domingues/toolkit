# Mocking Patterns

## Standard — `@Mock` + `@InjectMocks`

The dominant pattern. Use for all Use Cases and Persistence Adapters.

```java
@ExtendWith(MockitoExtension.class)
class ProjectUseCaseImplTest {

    @Mock
    private ProjectPersistencePort projectPersistencePort;

    @Mock
    private ProjectMapper projectMapper;

    @InjectMocks
    private ProjectUseCaseImpl useCase;
}
```

## Manual `mock()` in `@BeforeEach`

Use for Controller tests where MockMvc is built manually (no Spring context).

```java
class UserAPIControllerTest {

    private MockMvc mockMvc;
    private UserUseCase userUseCase;

    @BeforeEach
    void setUp() {
        userUseCase = mock(UserUseCase.class);
        UserAPIController controller = new UserAPIController(userUseCase);
        mockMvc = MockMvcBuilders.standaloneSetup(controller).build();
    }
}
```

## Stubbing

### Return a value

```java
when(port.findById(id)).thenReturn(Optional.of(entity));
when(port.findAll()).thenReturn(List.of(entity1, entity2));
```

### Throw an exception

```java
when(port.findById(id)).thenThrow(new AppException(Error.NOT_FOUND));
```

### Void methods

```java
doNothing().when(port).delete(id);
doThrow(new AppException(Error.NOT_FOUND)).when(port).delete(id);
```

### Dynamic response

Use `thenAnswer` when the return value depends on the input argument:

```java
when(repository.save(any(LibraryPromptEntity.class)))
    .thenAnswer(invocation -> invocation.getArgument(0));
```

## Verification

### Basic verify

```java
verify(port).getUserById(userId);
verify(port, times(1)).create(any(UserEntity.class));
```

### Verify never called

```java
verify(port, never()).delete(any());
verify(port, never()).findAllByProjectId(any());
```

### Verify no more interactions

```java
verifyNoMoreInteractions(libraryPromptUseCase);
verifyNoInteractions(libraryPromptMapper);
```

## `ArgumentCaptor` — Inspect What Was Passed

Use when you need to assert on the exact object passed to a mock, not just that it was called.

```java
@Test
void givenValidRequest_whenCreate_thenPersistWithCorrectFields() {
    when(port.create(any(LibraryPromptEntity.class))).thenReturn(savedEntity);

    useCase.createPrompt(request);

    ArgumentCaptor<LibraryPromptEntity> captor = ArgumentCaptor.forClass(LibraryPromptEntity.class);
    verify(port).create(captor.capture());

    LibraryPromptEntity captured = captor.getValue();
    assertThat(captured.getCreatedBy()).isEqualTo(userEntity);
    assertThat(captured.getLikeCount()).isEqualTo(0);
    assertThat(captured.getCreatedAt()).isNotNull();
}
```

## `argThat` — Inline Predicate Verification

Use for concise multi-field verification without a separate captor variable.

```java
verify(port).create(argThat(entity ->
    entity.getCreator().equals(requesterUser) &&
    entity.getProvider().equals(providerEntity) &&
    entity.getCertifier() == null &&
    entity.getDownloadCount() == 0 &&
    entity.getCreatedAt() != null
));

verify(port).update(argThat(entity ->
    entity.getDeletedAt() != null &&
    entity.getUpdatedAt() != null
));
```

Prefer `ArgumentCaptor` when you need to assert on many fields with descriptive failure messages. Prefer `argThat` for compact boolean checks.

## Static Mocking {#static-mocking}

Use `MockedStatic` from `mockito-inline` (already declared in `build.gradle`). Always close in `@AfterEach`.

```java
@ExtendWith(MockitoExtension.class)
class AccessManagementApiApplicationMainTest {

    private MockedStatic<SpringApplication> springApplicationMock;

    @BeforeEach
    void setUp() {
        springApplicationMock = mockStatic(SpringApplication.class);
    }

    @AfterEach
    void tearDown() {
        springApplicationMock.close(); // mandatory — leaks between tests if omitted
    }

    @Test
    void givenAppStarts_whenMain_thenDelegateToSpringApplication() {
        AccessManagementApiApplication.main(new String[]{});

        springApplicationMock.verify(
            () -> SpringApplication.run(AccessManagementApiApplication.class, new String[]{})
        );
    }
}
```

## Avoiding Unnecessary Stubbing

Only stub what the specific test needs. Unnecessary stubs cause `UnnecessaryStubbingException` with `MockitoExtension`.

```java
// BAD — stubs findAll even though this test only calls findById
when(port.findAll()).thenReturn(List.of());
when(port.findById(id)).thenReturn(Optional.of(entity));
useCase.getById(id);

// GOOD — only what this test uses
when(port.findById(id)).thenReturn(Optional.of(entity));
useCase.getById(id);
```

If a stub is needed in most but not all tests, move it to `@BeforeEach` and annotate the extension with `@MockitoSettings(strictness = Strictness.LENIENT)` — or restructure the tests.
