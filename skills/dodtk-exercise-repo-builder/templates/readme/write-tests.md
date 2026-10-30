# {{TITLE}}

{{DEADLINE_LINE}}<!-- Contexto do sistema já pronto, 1–2 frases. -->
A aplicação já está **completamente implementada**.

> ⚠️ **Regra principal: nenhum arquivo de código de produção deve ser modificado** (<!-- ex.: src/main/, src/, app/ -->).
> Sua tarefa é escrever **exclusivamente os testes** em <!-- ex.: src/test/, tests/, __tests__/ -->.

---

## 📐 Visão geral do sistema

<!-- Entidades, ciclo de vida/estados, regras principais. -->

## 📂 Entidades / módulos

| Campo | Tipo | Restrições |
|-------|------|------------|
| | | |

## 🎯 Objetivo

Criar testes unitários para:

- `<unidade 1>`
- `<unidade 2>`

A ferramenta de cobertura está configurada para medir **<!-- linhas | branches -->** em `<!-- pacote/pasta alvo -->`.
Os testes devem usar **<!-- mocks/stubs: Mockito, unittest.mock, jest.fn, Moq... -->** — sem banco real, sem rede, sem subir o servidor.

## 🗂️ Estrutura esperada dos testes

```
<!-- árvore de pastas dos testes -->
```

### Esqueleto de uma classe/arquivo de teste

```text
<!-- exemplo mínimo na stack, com setup de mocks -->
```

## 📋 Cenários obrigatórios por unidade

### 1. `<unidade>`

#### `<método/função>(…)`

| # | Cenário | Comportamento esperado |
|---|---------|------------------------|
| 1.1 | | |
| 1.2 | | lança/retorna `…` |

## 💡 Dicas

<!-- Snippets de: verificar exceção, verificar chamada do mock (times/never), configurar retorno, capturar argumento. -->

## 🏆 Critério de aprovação

A nota é proporcional à cobertura, em degraus:

| Cobertura | Pontos acumulados |
|-----------|-------------------|
| ≥ 10% | 1 |
| … | … |
| 100% | 10 |

Todo `if`/`else`, retorno antecipado e lançamento de erro precisa ser exercitado por pelo menos um teste.

```bash
python .github/classroom/grade.py
```

## 🚀 Como começar e entregar

1. Faça um **fork** (ou `git checkout -b resolucao/<seu-nome>`).
2. Escreva os testes, rode localmente, faça `git push`.
3. A nota aparece no workflow **Autograding**.
