# Anatomia de um repositório de treino

Modelo extraído de 11 repositórios reais (`exercicio-*`, `atividade-*`, `projeto-*`, todos criados a partir de um template e corrigidos automaticamente). Esta é a estrutura que a skill reproduz, seja qual for a stack.

## Ciclo de vida

```
[template do autor] --fork/branch--> [repo do aluno] --push--> [CI: autograding] --> nota
       |                                   |
  Initial commit                  commits de resolução
  (+ "add deadline")              (":tada: Finalizando atividade!")
```

1. O autor publica um repo-template com: enunciado completo, código starter que compila, testes prontos, pipeline de correção.
2. Cada aluno ganha uma cópia (fork, branch ou "use this template"). O histórico do aluno começa em `Initial commit`.
3. A cada `push` o workflow roda os testes declarados em `.github/classroom/autograding.json` e soma os pontos.
4. A nota é a do último run. Nada além do código do aluno muda entre runs.

## Estrutura de arquivos (invariante)

```
<repo>/
├── README.md                     # enunciado = contrato. Única fonte de instruções.
├── .gitignore / .gitattributes   # da stack + normalização de EOL para scripts (mvnw eol=lf, *.cmd eol=crlf)
├── <build/manifest da stack>     # pom.xml, package.json, pyproject.toml, *.csproj, go.mod...
├── <wrapper do build>            # mvnw, gradlew... (quando a stack tiver) para não depender do ambiente
├── <código de produção>          # starter: completo onde não é objeto do exercício, esqueleto onde é
├── <testes>                      # o "método de asserção" — prontos e versionados (exceto no tipo write-tests)
│   └── resources/fixtures        # request/ response/ datasets/input datasets/expected  features/ ...
├── <assets opcionais>            # imagens do enunciado (.github/screenshots/, gato.jpeg...)
└── .github/
    ├── classroom/autograding.json   # lista de testes → comando → pontos
    └── workflows/classroom.yml      # checkout → setup da stack → build → autograder
```

## Camadas de um exercício

| Camada | Papel | Onde |
|--------|-------|------|
| Contexto | narrativa realista (clínica, banco, biblioteca, evento) que justifica as regras | topo do README |
| Contrato | nomes, assinaturas, rotas, formatos, códigos de erro — exatamente o que os testes exigem | README (tabelas + exemplos) |
| Restrições | o que não pode (alterar `src/main`, libs externas, frameworks) e regras de arquitetura | README "Atenção"/"Restrições" |
| Starter | estrutura pronta + pontos de implementação marcados com `TODO` e retorno neutro | código |
| Asserção | testes automatizados agrupados por funcionalidade | pasta de testes + fixtures |
| Pontuação | cada grupo de teste = 1 entrada no autograding.json com `points` | `.github/classroom/` |
| Pipeline | executa a pontuação a cada push, em ambiente limpo | `.github/workflows/` |

## Padrões recorrentes

- **README dirige tudo.** Seções típicas: título com emoji, 🎯 Objetivo, ⚠️ Atenção, 📌 Requisitos gerais, 📂 Modelo, 🔧 Endpoints/Funcionalidades numeradas (1️⃣ 2️⃣ …), 🔥 Desafio, tratamento de erros (tabela situação → status), 🏢 regras de arquitetura, 💡 Dicas, frase de encerramento.
- **Cenários testados explícitos.** Cada funcionalidade lista entrada → saída esperada. O aluno sabe exatamente o que será verificado (exceto no tipo fix-bug).
- **Starter que compila mas não pontua.** Ex.: `return null;`, `throw new UnsupportedOperationException("Não implementado ainda.")`, `ResponseEntity.internalServerError().build()`, cada um com `// TODO: Implemente o código`.
- **Fixtures fora do código de teste.** JSON de request/response esperados e datasets de banco (antes/depois) em arquivos separados, lidos por um utilitário (`FileUtil.readFile`).
- **Casos inválidos parametrizados.** Um provider lista N arquivos inválidos → um teste parametrizado espera o mesmo erro (400) para todos.
- **Grupos de teste = unidade de nota.** Classe aninhada por endpoint (`MusicaTest$PostMusica`), método individual, tag BDD (`@cadastrar-duplicado`) ou degrau de cobertura (`coverage-50`).
- **Dificuldade graduada.** Aquecimento → fácil 👶 → médio ⚖️ → difícil 💪 / desafio 🔥; pontos 1/2/3.
- **Ambiente de teste isolado.** Banco em memória, perfil/config de teste, dados resetados antes de cada teste, IDs com sequência reiniciada.
- **Prazo no README.** Commit "add deadline" insere badge/linha de prazo no topo.

## Estratégia de resolução (lado do aluno)

- Fork (ou branch `resolucao/<nome>`) a partir do template → implementa → `push` → lê o relatório do CI → repete.
- O aluno pode rodar a mesma correção localmente (`python .github/classroom/grade.py`), garantindo paridade com o CI.
