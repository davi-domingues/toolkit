# Stack: Go

Perfil do scaffold: `go`. Runner: `go test` (stdlib).

## Layout
```
go.mod
internal/<dominio>/...      # produção (starter)
internal/<dominio>/*_test.go
testdata/{request,response,datasets}/   # diretório ignorado pelo build, convenção do Go
```

## Seletores
```bash
go test ./internal/usuarios -run '^TestPostUsuario$' -count=1
go test ./... -run 'TestUsuarios/POST' -count=1          # subtestes t.Run
```
`-run` sem correspondência imprime "no tests to run" e **passa** — adicione um teste que sempre roda no pacote e falha no starter, ou valide no verify que cada entrada reprova no starter.

## Padrões
- **HTTP:** `httptest.NewRecorder()` + `handler.ServeHTTP`, ou `httptest.NewServer`.
- **Golden:** decode para `any` dos dois lados e `reflect.DeepEqual`; ou golden files com flag `-update` (só para o autor).
- **Tabela de casos:** `[]struct{name, in, want}` + `t.Run(tc.name, ...)` — cada nome vira seletor.
- **Banco:** SQLite (`modernc.org/sqlite`, sem CGO) em memória ou interface de repositório com fake.
- **Arquitetura:** teste que roda `go list -deps ./internal/handlers/...` e falha se aparecer `internal/repository`; ou `go-arch-lint`.

## Cobertura em degraus
```bash
go test ./internal/service/... -covermode=atomic -coverprofile=cover.out
go tool cover -func=cover.out | tail -1          # total: (statements) NN.N%
```
Gate por script: `awk` no total ≥ limiar. Go não mede branches nativamente (cobertura de statements).

## Starter idioms
```go
func EhPrimo(n int) bool {
	panic("TODO: implemente") // ou return false se o teste exigir true para algum caso
}
```
Cuidado: retorno zero-value (`false`, `0`, `""`) pode passar em casos negativos — prefira `panic` no starter.
