---
name: dodtk-quality-review
description: Review semântica de qualidade restrita às mudanças de uma branch, em 3 fases com aprovação - plano (arquivo e linha), aplicação e commit de refactor. Use para limpar código morto, duplicação, smells e comentários antes de integrar.
---

# Quality Review (revisão → aprovação → commit)

Contexto informado pelo usuário (branch, base, repositório, restrições): $ARGUMENTS

Se algo não foi informado, descubra sozinho: a branch é a atual; a base é a branch de onde ela saiu (`git merge-base` com `main`/`master`/`develop` ou a branch de integração que o usuário citar). Confirme a base em uma linha antes de seguir.

## Regras gerais

- Escopo: SOMENTE o que a branch introduziu (`git diff <base>...HEAD`). Código que já existia na base não é alterado, mesmo que tenha problemas. Nesse caso, liste à parte como "fora do escopo".
- Antes de mudar qualquer coisa, leia as configs do projeto (package.json, pom.xml, Makefile, pyproject etc.) para achar os comandos de build, teste e lint. Rode-os e registre a linha de base (o que já falhava antes).
- Nunca stageie arquivos de ambiente ou de configuração local que o usuário tenha modificado (ex.: `environment.local.*`, `.env*`), nem arquivos fora do escopo. Use `git add <caminho>` por arquivo, nunca `git add .`. Não mexa no `.gitignore` por conta própria.
- Não faça push, rebase, reset --hard nem apague branches sem pedir.

## Fase 1: Revisão e plano (sem alterar arquivos)

1. Liste os arquivos e trechos alterados pela branch (`git diff --stat` e os hunks).
2. Faça uma revisão semântica dos trechos e agrupe os achados por categoria:
   - A. Imports e código mortos (imports sem uso ou duplicados, variáveis, funções, estilos e arquivos que nada usa)
   - B. Duplicação (lógica, templates ou estilos repetidos que podem ser extraídos)
   - C. Code smells e inconsistências (strings soltas que deveriam ser constantes, nomes fora do padrão do projeto, tipagem frouxa, bugs visuais ou de formatação, padrões divergentes do resto da base)
   - D. Comentários avulsos ou desnecessários adicionados pela branch
   - E. Débitos técnicos (TODOs, marcadores temporários, mocks esquecidos, testes faltando)
3. Apresente o plano de ação como tabela: `ID | Categoria | Arquivo:linha | Problema | Ação proposta | Risco de comportamento`.
4. Separe o que está fora do escopo (já existia na base) e o que precisa de decisão do usuário.
5. PARE e peça aprovação. O usuário pode aprovar tudo, aprovar parte ou mudar regras por categoria (ex.: "remova todos os comentários", "garanta que B e C não quebram comportamento").

## Fase 2: Aplicação (depois da aprovação)

1. Aplique só os itens aprovados, seguindo as observações do usuário, que valem mais que o plano.
2. Refactors de B e C devem preservar o comportamento: mesma saída, mesmos eventos, mesma renderização. Escreva testes para cada extração nova (helper, componente, função) seguindo o framework e o padrão de testes do projeto.
3. Se o usuário pedir zero comentários, a informação que for relevante sai do código e vai para a documentação do projeto (README, docs, ADR), nunca se perde.
4. Ao final, rode build, testes e lint. Não pode haver falha nova em relação à linha de base. Se houver, corrija antes de seguir.
5. Mostre um resumo: o que foi aplicado por ID, o que foi ignorado e por quê, e o resultado da verificação.

## Fase 3: Commit (com validação)

1. Stageie por caminho só os arquivos do refactor e confira com `git diff --cached --name-only`. Arquivos locais e protegidos devem ficar de fora.
2. Proponha a mensagem no padrão de commits do repositório (veja `git log`). Padrão sugerido: título `refactor: melhoria de qualidade do código` e uma descrição curta (2 ou 3 linhas) do que mudou.
3. Mostre a lista de arquivos staged e a mensagem. PARE e peça aprovação.
4. Aplique os ajustes pedidos (título, descrição), faça o commit sem `--no-verify` e mostre o hash. Não faça push.
