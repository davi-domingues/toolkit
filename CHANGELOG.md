# Changelog

## 0.2.0
- Pacote `@davi-domingues/toolkit` com o comando `toolkit` (`bin/toolkit.js`), publicado no GitHub Packages.
- Workflow `publish` em tag `vX.Y.Z`: confere tag x versao, roda validate e testes, publica com `GITHUB_TOKEN` e cria o GitHub Release.
- `validate` sai com codigo 1 quando ha skill invalida.

## 0.1.0
- Estrutura `skills/ agents/ rules/ prompts/` e skills existentes movidas para `skills/`.
- `java-testing-patterns` passa a ser versionada.
- Instalador `scripts/toolkit.mjs` (install, uninstall, status, validate) para Kiro, Claude e OpenCode.
- Testes com `node --test` e CI no GitHub Actions.
- README reescrito e prompt orquestrar adicionado.
- README em ingles e licenca MIT.
