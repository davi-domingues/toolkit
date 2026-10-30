# Stack: Python

Perfil do scaffold: `python`. Runner: **pytest**.

## Layout
```
pyproject.toml (ou requirements.txt com versões fixas: pytest==x.y.z)
src/<pacote>/ ou <pacote>/      # produção (starter)
tests/test_*.py  tests/fixtures/{request,response,datasets}/  tests/conftest.py
```
Use `pytest.ini`/`[tool.pytest.ini_options]` com `testpaths = ["tests"]` e `pythonpath = ["src"]`.

## Seletores
```bash
python3 -m pytest -q tests/test_usuarios.py::TestPostUsuario      # classe = grupo
python3 -m pytest -q -k "post and duplicado"
python3 -m pytest -q -m desafio                                     # marker
behave --tags=@cadastrar-duplicado                                  # BDD
```
`pytest` retorna exit 5 quando nenhum teste é coletado — isso reprova (bom: seletor errado não dá ponto).

## Padrões
- **HTTP:** FastAPI `TestClient(app)`, Flask `app.test_client()`, Django `Client`.
- **Golden:** `assert resp.json() == json.loads((FIX / "response/x.json").read_text("utf-8"))`.
- **Banco:** SQLite em memória (`sqlite:///:memory:` + `StaticPool`), fixture `db` que cria schema e carrega `datasets/input/*.json`; compare tabela inteira com `datasets/expected`.
- **Inválidos:** `@pytest.mark.parametrize("arquivo", [...], ids=[...])`.
- **Mocks (write-tests):** `unittest.mock` / `pytest-mock` (`mocker.patch.object(repo, "find_by_id", return_value=None)`).
- **Arquitetura:** `import-linter` (contracts `forbidden`/`layers` em `.importlinter`; `lint-imports`) ou teste que percorre `ast` dos módulos e falha em imports proibidos.
- **I/O de script:** `subprocess.run([sys.executable, "main.py"], input=..., capture_output=True)` ou o próprio `input`/`output` do autograding.
- **Tipos/estilo:** `mypy src`, `ruff check src`.

## Cobertura em degraus
```bash
python3 -m pytest -q --cov=src/app/services --cov-branch --cov-fail-under=50
```
Ou rode uma vez no `setup` (`coverage run --branch -m pytest`) e cada degrau `coverage report --include='src/app/services/*' --fail-under=50`. Mutação: `mutmut run` + `mutmut results`.

## Starter idioms
```python
def eh_primo(n: int) -> bool:
    # TODO: implemente
    raise NotImplementedError
```
