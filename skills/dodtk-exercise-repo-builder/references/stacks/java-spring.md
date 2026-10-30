# Stack: Java (Spring Boot / Maven ou Gradle)

Stack de todos os exemplos analisados. Perfil do scaffold: `java-maven` (ou `java-gradle`).

## Layout
```
pom.xml  mvnw  mvnw.cmd  .mvn/wrapper/maven-wrapper.properties
src/main/java/<pkg>/{controller,service,repository,entity,dto/{request,response},mapper,exception}/
src/main/resources/application.properties   schema.sql (JDBC)
src/test/java/<pkg>/{<Recurso>Tests.java, LayeredArchitectureTests.java, provider/, util/FileUtil.java}
src/test/resources/{application.properties|application-test.properties, request/, response/, datasets/{input,expected,schema}/, features/}
```
Gere o projeto base com Spring Initializr (`curl https://start.spring.io/starter.zip -d dependencies=web,validation,data-jpa,h2 -d javaVersion=21 -d type=maven-project ...`) ou copie wrapper de um projeto existente. Inclua o wrapper — o CI usa `./mvnw`.

## Dependências de teste (pin de versão)
| Uso | Artefato |
|-----|----------|
| Base | `spring-boot-starter-test` |
| Datasets de banco | `com.github.database-rider:rider-junit5` (ou `rider-spring`) |
| Arquitetura | `com.tngtech.archunit:archunit-junit5` |
| BDD | `io.cucumber:cucumber-java`, `cucumber-spring`, `cucumber-junit-platform-engine` + `org.junit.platform:junit-platform-suite` |
| Cobertura | plugin `org.jacoco:jacoco-maven-plugin` |
| Mutação | plugin `org.pitest:pitest-maven` + `pitest-junit5-plugin` |

## Seletores para o autograding
```bash
./mvnw -q test -Dtest='MusicaTest$PostMusica'                 # classe aninhada (@Nested)
./mvnw -q test -Dtest='EventoControllerTest#criarEventoComSucesso'
./mvnw -q test -Dtest='LayeredArchitectureTests'
./mvnw -q test -Dcucumber.filter.tags='@cadastrar-duplicado'
```
Acrescente `-DargLine="-Dfile.encoding=UTF-8"` se houver acentos em fixtures. Use `-Dsurefire.failIfNoSpecifiedTests=true` (padrão) para que seletor errado falhe. Timeout: 5–10 min (boot do contexto + download no 1º run).

## Padrões de teste
- **HTTP:** `@SpringBootTest(webEnvironment = RANDOM_PORT)` + `TestRestTemplate`, ou `@AutoConfigureMockMvc` + `MockMvc`. Para katas: `@WebMvcTest(Controller.class)`.
- **Golden JSON:** `objectMapper.readTree(body)` vs `readTree(FileUtil.readFile("/response/x.json"))` → `assertEquals` (compara árvore).
- **Datasets:** `@DBRider`, `@DBUnit(cacheConnection=false, alwaysCleanAfter=true)`, `@DataSet("datasets/input/x.json")`, `@ExpectedDataSet(value="datasets/expected/y.json", compareOperation=CONTAINS)`; script `datasets/schema/set-auto-increment.sql` com `ALTER TABLE t ALTER COLUMN id RESTART WITH n` em `executeScriptsBefore`.
- **Inválidos:** `@ParameterizedTest(name="{0}") @ArgumentsSource(InvalidXProvider.class)` com `Arguments.of("descrição", "arquivo.json")`.
- **Agrupamento:** `@Nested @DisplayName("POST /recurso") class PostRecurso {}` → uma entrada no autograding.
- **Arquitetura:** `noClasses().that().resideInAPackage("..controller..").should().dependOnClassesThat().resideInAnyPackage("..repository..","..entity..")`.
- **Esquema:** `@SpringBootTest(properties="spring.jpa.hibernate.ddl-auto=validate")` com `schema.sql` versionado.
- **Datas:** fixtures com `2099-…`; para "hoje", calcule no teste (`LocalDate.now()`).
- **Banco de teste:** H2 em memória, `spring.jpa.hibernate.ddl-auto=create-drop`, `spring.sql.init.data-locations=` (desliga seed de dev).

## Cobertura em degraus (write-tests)
Opção A (uma execução por degrau, sem profiles):
```xml
<execution><id>check-coverage-50</id><goals><goal>check</goal></goals>
  <configuration>
    <includes><include>com/acme/app/service/*</include></includes>
    <rules><rule><element>PACKAGE</element><limits><limit>
      <counter>BRANCH</counter><value>COVEREDRATIO</value><minimum>0.50</minimum>
    </limit></limits></rule></rules>
  </configuration></execution>
```
autograding: 1ª entrada `setup: "./mvnw -q test jacoco:report"`, `run: "./mvnw -q jacoco:check@check-coverage-10"`; demais só o `run`.
Opção B: uma execução `default-cli` com `<minimum>${jacoco.coverage.minimum}</minimum>` e `-Djacoco.coverage.minimum=0.5` no `run` (dispensa 10 profiles).
Prepare-agent precisa estar ligado (`<goal>prepare-agent</goal>`).

## Starter idioms
```java
// TODO: Implemente o código
public List<Empresa> listar() { throw new UnsupportedOperationException("Não implementado ainda."); }

@GetMapping("/{id}")  // TODO: Implemente o código
public ResponseEntity<EmpresaResponse> buscarPorId(@PathVariable Long id) { return ResponseEntity.internalServerError().build(); }
```
Entidades/DTOs vazios precisam compilar com o que os testes referenciam (testes que usam getters → crie a classe com os campos, ou deixe os testes só no nível HTTP).

## .gitattributes
`/mvnw text eol=lf`, `*.cmd text eol=crlf`; e `git update-index --chmod=+x mvnw`.

## Ambiente local
Exige JDK compatível com `<java.version>` (21). JDK 8 não compila Spring Boot 3 — se não houver JDK adequado, não dá para validar localmente; avise o usuário e confie no CI.
