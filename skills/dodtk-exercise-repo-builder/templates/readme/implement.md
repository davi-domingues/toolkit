# {{TITLE}}

{{DEADLINE_LINE}}<!-- 1–3 parágrafos de contexto: quem é o "cliente", qual o problema, por que isso importa. -->

## 🎯 Objetivo

<!-- Uma frase: o que deve ser construído, com qual stack ({{STACK_LABEL}}). -->

## ⚠️ Atenção

1. Sua nota é a soma dos pontos dos testes que passarem (veja [Avaliação](#-avaliação)).
2. O projeto precisa **compilar/rodar sem erros** — erro de build zera todos os testes.
3. Respeite **exatamente** os nomes, rotas, formatos e códigos de status descritos. Os testes dependem deles.
4. **Não altere** os arquivos de teste nem `.github/` (o pipeline compara com o original).
5. <!-- Restrições: bibliotecas proibidas, "use apenas o visto em aula", etc. -->

## 📌 Requisitos gerais

<!-- Porta, recurso base, convenções (ex.: lista vazia → 204, erro de validação → 400). -->

## 📂 Modelo / Estrutura

<!-- Tabela de entidades/estruturas: campo | tipo | restrições. Ou layout de pastas esperado. -->

| Campo | Tipo | Restrições |
|-------|------|------------|
| | | |

## 🔧 Funcionalidades

<!-- Uma seção numerada por item do contrato. Para cada uma: objetivo, assinatura/rota, regras, exemplo de entrada e saída. -->

### 1️⃣ <!-- Nome -->

**Objetivo:** …

- **Chamada / Endpoint:** `…`
- **Regras:**
  - …
- **Retornos:** sucesso `…` · erro `…`

#### Exemplo

```text
entrada → saída
```

---

### 🔥 Desafio

<!-- Itens extras, mais difíceis, com mais pontos. Opcional. -->

## 🚦 Tratamento de erros

| Situação | Resultado esperado |
|----------|--------------------|
| | |

## 🧪 Como rodar os testes

```bash
# todos os testes, com a nota calculada igual ao pipeline
python .github/classroom/grade.py

# só um grupo (regex no nome do teste)
python .github/classroom/grade.py -k "1\."

# comando nativo da stack
<!-- ex.: ./mvnw test | npm test | pytest | dotnet test | go test ./... -->
```

## 🏆 Avaliação

| # | Cenário | Pontos |
|---|---------|--------|
| | | |

Total: **__ pontos**. Os testes rodam a cada `push` no workflow **Autograding** (aba *Actions*).

## 🚀 Como começar e entregar

1. Faça um **fork** deste repositório (ou crie uma branch: `git checkout -b resolucao/<seu-nome>`).
2. Clone, implemente e rode os testes localmente.
3. Faça commits pequenos e `git push`. Cada push dispara a correção automática.
4. A nota final é a do último run antes do prazo.

## 💡 Dicas

- <!-- Dicas pontuais (API útil, armadilha comum). Nunca a solução. -->
