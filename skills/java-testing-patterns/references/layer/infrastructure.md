# Infrastructure / Config Testing Rules

**Location:** `src/test/java/.../infrastructure/`

Tests for configuration beans, global exception handlers, and security settings.

## Core Principles
1. **Direct Instantiation**: Treat configurations as simple classes. Instantiate them directly without loading the Spring Context.
2. **Validate Configurations**: Check that the created configuration objects (like `OpenAPI` or `CorsConfiguration`) hold the expected hardcoded values or structures.

## Rules & Restrictions
- **No `@SpringBootTest`**: Do not boot the application to test a configuration bean.
- **Exception Handlers**: When testing a `@ControllerAdvice` / `GlobalExceptionHandler`, instantiate it directly, pass a fake exception, and verify the `ResponseEntity` returned.

## Generic Skeleton

```java
class <Config>Test {

    @Test
    void givenConfigClass_whenMethodCalled_thenReturnExpectedConfiguration() {
        // Arrange
        // <Config>Class config = new <Config>Class();

        // Act
        // Object result = config.someBeanMethod();

        // Assert
        // assertNotNull(result);
        // assertEquals("Expected Value", result.getProperty());
    }
}
```