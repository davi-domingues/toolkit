# Controllers Testing Rules

**Location:** `src/test/java/.../adapter/in/api/`

Controllers handle HTTP requests, validate input, and delegate to Use Cases.

## Core Principles
1. **No Spring Context**: NEVER use `@WebMvcTest` or `@SpringBootTest`.
2. **Standalone MockMvc**: Always instantiate `MockMvc` manually using `MockMvcBuilders.standaloneSetup()`.
3. **Mock Use Cases**: Use Cases are mocked manually (`mock(UseCase.class)`) inside `@BeforeEach` and passed into the controller's constructor.
4. **Test HTTP Semantics**: Focus on Status Codes, Headers, and JSON structure, NOT business logic.

## Rules & Restrictions
- **Do not test business logic here**: If testing a complex calculation or rule, move that test to the Use Case.
- **Serialization**: Use a standard `new ObjectMapper()` to convert DTOs to JSON strings for request bodies.
- **Pagination**: If the endpoint accepts `Pageable`, you MUST configure `.setCustomArgumentResolvers(new PageableHandlerMethodArgumentResolver())` in the `standaloneSetup`.

## Generic Skeleton

```java
class <Domain>APIControllerTest {

    private MockMvc mockMvc;
    private <Domain>UseCase useCase;
    private final ObjectMapper objectMapper = new ObjectMapper();

    @BeforeEach
    void setUp() {
        useCase = mock(<Domain>UseCase.class);
        <Domain>APIController controller = new <Domain>APIController(useCase);
        mockMvc = MockMvcBuilders.standaloneSetup(controller).build();
    }

    @Test
    void givenValidRequest_whenEndpoint_thenReturnExpectedStatusAndJson() throws Exception {
        when(useCase.action(any())).thenReturn(expectedResponse);

        mockMvc.perform(post("/api/v1/<resource>")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.field").value("expectedValue"));

        verify(useCase).action(any());
    }

    @Test
    void givenInvalidCondition_whenEndpoint_thenReturnErrorStatus() throws Exception {
        doThrow(new AppException(Error.<ERROR_CODE>)).when(useCase).delete(id);

        mockMvc.perform(delete("/api/v1/<resource>/{id}", id))
                .andExpect(status().isNotFound());

        verify(useCase).delete(id);
    }
}
```

When the endpoint accepts `Pageable`, build the `MockMvc` with the resolver:

```java
mockMvc = MockMvcBuilders.standaloneSetup(controller)
        .setCustomArgumentResolvers(new PageableHandlerMethodArgumentResolver())
        .build();
```