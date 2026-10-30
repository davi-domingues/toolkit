# Stack: C# / .NET

Perfil do scaffold: `dotnet`. Runner: **xUnit** (NUnit/MSTest equivalentes).

## Layout
```
<Nome>.sln
src/<Nome>.Api/            # produção (starter)
tests/<Nome>.Tests/        # xUnit; fixtures em tests/<Nome>.Tests/Fixtures (CopyToOutputDirectory)
```

## Seletores
```bash
dotnet test --no-build --filter "FullyQualifiedName~UsuariosTests.Post"
dotnet test --filter "Category=Desafio"          # [Trait("Category","Desafio")]
```
Filtro sem correspondência não falha por padrão: confirme no starter que cada entrada reprova (ou combine com um teste "smoke" que sempre roda e falha no starter).

## Padrões
- **HTTP:** `WebApplicationFactory<Program>` (`Microsoft.AspNetCore.Mvc.Testing`) + `HttpClient`; exponha `public partial class Program {}`.
- **Golden:** `JsonNode.DeepEquals(JsonNode.Parse(body), JsonNode.Parse(File.ReadAllText("Fixtures/response/x.json")))`.
- **Banco:** EF Core com SQLite in-memory (`DataSource=:memory:` com conexão aberta) substituindo o DbContext na factory; seed por fixture.
- **Inválidos:** `[Theory] [MemberData(nameof(Invalidos))]`.
- **Mocks:** Moq / NSubstitute.
- **Arquitetura:** NetArchTest.Rules (`Types.InAssembly(...).That().ResideInNamespace("X.Controllers").ShouldNot().HaveDependencyOn("X.Repositories")`).
- **BDD:** Reqnroll (sucessor do SpecFlow), tags → `--filter "Category=tag"`.

## Cobertura em degraus
`coverlet.msbuild`: `dotnet test /p:CollectCoverage=true /p:Include="[*]*.Services.*" /p:Threshold=50 /p:ThresholdType=branch`. Mutação: Stryker.NET (`dotnet stryker --break-at 60`).

## Starter idioms
```csharp
public Usuario BuscarPorId(long id) => throw new NotImplementedException(); // TODO
```
Env: o runner preserva o ambiente (HOME/DOTNET_CLI_HOME), diferentemente do `education/autograding` antigo.
