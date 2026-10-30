# Pipeline de correção

## autograding.json (formato GitHub Classroom)

Local fixo: `.github/classroom/autograding.json`. É o contrato entre testes e nota — manter esse formato garante compatibilidade com o Classroom (se ainda estiver disponível para o usuário) e com `grade.py`.

```json
{
  "tests": [
    {
      "name": "2.3. POST /usuarios - cria usuário",
      "setup": "",
      "run": "<comando que roda SÓ este grupo>",
      "input": "",
      "output": "",
      "comparison": "included",
      "timeout": 10,
      "points": 2
    }
  ]
}
```

| Campo | Regra |
|-------|-------|
| `name` | Único. Prefixe com numeração do README (`1.2.`) e/ou `[2pts]`. Descreva o cenário, não o método. |
| `setup` | Opcional. Roda antes do `run`; se falhar, o teste reprova. Use para preparar algo uma vez (ex.: gerar relatório de cobertura na 1ª entrada). |
| `run` | Obrigatório. Exit code 0 = passou (quando `output` vazio). Deve ser **seletivo**: um grupo, não a suíte inteira. |
| `input` | stdin opcional. |
| `output` + `comparison` | Opcional. `included` (substring), `exact` (normaliza espaços finais/CRLF), `regex`. Use só em I/O puro. |
| `timeout` | **Minutos** (semântica do Classroom). JVM/.NET com contexto pesado: 5–10. Scripts: 1–2. |
| `points` | Inteiro ≥ 0. Soma = nota máxima. |
| `required` | Extensão do grade.py (ignorada pelo Classroom). Se `true` e reprovar, a nota inteira vira 0. Use para integridade. |

### Granularidade
- 1 entrada por **funcionalidade** (classe aninhada/describe/tag) → nota parcial justa, poucos boots do runtime.
- 1 entrada por **cenário** → feedback fino, mas N boots (lento em JVM). Vale para katas e suítes rápidas.
- Seletores por stack estão em `stacks/<stack>.md` (ex.: `-Dtest='Classe$Nested'`, `npx vitest run -t "nome"`, `pytest -k`, `dotnet test --filter`, `go test -run`).
- Entre aspas simples no `run` quando houver `$` ou `#` (o runner usa bash no Linux e Git Bash no Windows).

## grade.py (runner)

Copiado para `.github/classroom/grade.py` pelo scaffold. Stdlib apenas, Python 3.8+.

```bash
python .github/classroom/grade.py                 # nota completa (igual ao CI)
python .github/classroom/grade.py --validate      # só valida o JSON
python .github/classroom/grade.py --list
python .github/classroom/grade.py -k "POST"       # filtra por regex no nome
python .github/classroom/grade.py --junit r.xml --json r.json --fail-under 70
```

- Executa `setup`/`run` na raiz do repo; Windows usa Git Bash se existir (para `./mvnw`, `chmod`, `$`), senão `cmd`.
- Exit code: 0 se `percent >= --fail-under` (padrão 100), 1 caso contrário, 2 erro de configuração. Em CI isso deixa o check verde só com nota máxima; use `--fail-under 0` ou `--no-fail` se preferir sempre verde.
- Em GitHub Actions escreve tabela de nota em `$GITHUB_STEP_SUMMARY`.

## Workflows

### GitHub Actions — `templates/ci/github-workflow.yml`
Gerado em `.github/workflows/classroom.yml`: checkout → setup da stack (de `stacks.json`) → build sem testes (`continue-on-error`) → `grade.py` → upload do relatório. Trigger em push de qualquer branch, PR para main e manual.

### GitLab CI — `templates/ci/gitlab-ci.yml`
Imagem da stack, `before_script` com build, `grade.py --junit` como `reports: junit` (aparece na aba Tests do MR).

### Outros (Azure Pipelines, Jenkins, Bitbucket, local)
Qualquer CI serve: precisa de Python 3 + toolchain da stack, depois `python3 .github/classroom/grade.py --junit grading-report.xml`. Publique o XML como relatório de testes.

### GitHub Classroom (opcional)
O workflow original usava `education/autograding@v1`, que lê o mesmo JSON. O GitHub anunciou o encerramento do Classroom (agosto/2026) e as actions do Classroom foram marcadas como deprecated. Por isso o padrão gerado usa `grade.py`. Se o usuário ainda usa Classroom, mantenha o JSON e troque o step final por `uses: education/autograding@v1` (permissões `checks: write`, `actions: read`, `contents: read`).

## Fork vs branch (como o aluno trabalha)

| Modelo | Como | Quando |
|--------|------|--------|
| Template + fork/"Use this template" | autor marca o repo como template; cada aluno cria o seu | turmas, avaliação individual |
| Branch por tentativa | `git checkout -b resolucao/<nome>`; workflow roda em todas as branches | estudo individual, várias tentativas no mesmo repo |
| Branch `solucao` (autor) | gabarito numa branch que **não** é publicada para alunos | autoestudo; nunca no template de turma |

O workflow dispara em `push` para `**` — funciona nos três modelos.
