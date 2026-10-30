# Outras stacks e plataformas

Para qualquer coisa fora de `java-spring`, `node`, `python`, `dotnet`, `go`: aplique o mesmo modelo — **um comando por grupo de testes que retorna exit 0 só quando o grupo passa**. Se a ferramenta não seleciona testes, escreva um script por grupo (`tests/run_<grupo>.sh`).

## Rust (`rust`)
`cargo test --test usuarios post_` (filtro por substring; `-- --exact` para nome exato). Fixtures em `tests/fixtures`. HTTP: `axum` + `tower::ServiceExt::oneshot`. Cobertura: `cargo llvm-cov --fail-under-lines 50`. Starter: `todo!()` (panic → reprova).

## PHP (`php`)
PHPUnit: `vendor/bin/phpunit --filter 'UsuarioTest::testPost'` ou `--group desafio`. Laravel: `php artisan test --filter=...`, `RefreshDatabase` + SQLite memória. Cobertura: `--coverage-text` + checagem (pcov/xdebug). Arquitetura: `pestphp/pest-plugin-arch` ou deptrac. Starter: `throw new \LogicException('TODO');`.

## Ruby (`ruby`)
RSpec: `bundle exec rspec spec/usuarios_spec.rb -e "POST"` ou `--tag desafio`. Rails request specs + `rails db:test:prepare`. Cobertura: SimpleCov `minimum_coverage`. Starter: `raise NotImplementedError`.

## C / C++ (`c-cpp`)
Testes com Unity/CMocka (C) ou GoogleTest/Catch2 (C++): `ctest --test-dir build -R '^usuarios_post$' --output-on-failure` ou `./build/tests --gtest_filter='Usuarios.*'`. Katas de I/O: compile e use `input`/`output` do autograding (`"run": "gcc -O2 -o a main.c && ./a"`). Cobertura: gcovr `--fail-under-line`.

## Front-end puro (HTML/CSS/JS vanilla) (`node` como toolchain de teste)
Asserções: Playwright contra `index.html` servido localmente (seletores definidos no README), checagem estática de restrições (nenhum `<script src=...cdn...>` de framework, nenhum `import` de lib, `package.json` sem deps de runtime), validação HTML (`html-validate`). Back-end separado segue a própria stack.

## SQL / banco de dados (`generic` ou `python`)
Aluno escreve `queries/*.sql`. Teste carrega schema + dataset em SQLite/PostgreSQL (service container no CI) e compara o resultado da query com `expected/*.csv` (ordem normalizada salvo se o enunciado pedir `ORDER BY`). Um teste por query.

## Infra / DevOps (Docker, Terraform, Kubernetes, shell) (`generic`)
- Docker: `docker build` passa; `docker run` + `curl` no healthcheck; `hadolint Dockerfile`.
- Compose: `docker compose config -q`; subir e testar endpoints.
- Terraform: `terraform fmt -check`, `terraform validate`, `terraform plan` com provider mock/localstack, `conftest`/OPA para políticas.
- Kubernetes: `kubeconform`, `kind` no CI para aplicar e checar rollout.
- Shell: `bats` (`bats tests/ -f "nome"`), `shellcheck`.

## Mobile, dados, ML, etc.
Mesmo princípio: separe "contrato" (função/endpoint/arquivo gerado) de "verificação" (script que compara com esperado e devolve exit code). Notebooks: converta e execute (`jupyter nbconvert --execute`) e teste funções extraídas para `src/`; métricas de modelo com limiar (`accuracy >= 0.85`) em degraus.

## Plataformas de CI
GitHub Actions e GitLab CI têm template. Para outras, ver `grading-pipeline.md` § Outros. Se o runtime não tiver action de setup, use imagem de container no job (`container: <imagem>` no GitHub Actions).
