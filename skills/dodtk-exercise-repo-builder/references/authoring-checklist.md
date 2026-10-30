# Checklist de autoria

Use antes de entregar o repo. Itens marcados (V) são verificados automaticamente por `scripts/verify.py`.

## Contrato
- [ ] Todo cenário do README tem pelo menos um teste; todo teste corresponde a uma frase do README (exceto fix-bug, onde o README é vago de propósito).
- [ ] Nomes de arquivos/classes/funções/rotas/campos no README são idênticos aos usados nos testes.
- [ ] Exemplos de request/response do README são os mesmos JSONs das fixtures (copie, não redigite).
- [ ] Tabela de erros (situação → status/exceção) completa.
- [ ] Nada que o aluno precise saber está só no código de teste.

## Starter
- [ ] Compila/instala sem erros em ambiente limpo (V: o starter roda inteiro no verify).
- [ ] Nenhum teste pontuável passa (V: starter = 0%, ou ≤ `--starter-max`). Retornos neutros que reprovam: `null`, exceção "não implementado", status 500, lista vazia só quando o teste exige conteúdo.
- [ ] Cada ponto de implementação tem `TODO` com o mesmo vocabulário do README.
- [ ] Nenhum resquício da solução (comentários, código morto, branch publicada, histórico git).

## Testes
- [ ] Gabarito passa em 100% (V).
- [ ] Testes determinísticos: sem dependência de hora atual (ou datas relativas a "hoje"/datas futuras longe), ordem, rede, porta fixa, aleatoriedade sem seed.
- [ ] Datas em fixtures que dependem de "futuro" usam ano distante (ex.: 2099) — o exercício não pode "vencer".
- [ ] Estado isolado entre testes (limpeza antes de cada um, IDs reiniciados).
- [ ] Mensagens de falha legíveis (nome do teste descreve o cenário em linguagem do aluno).
- [ ] Testes de "não deve alterar o banco" em operações inválidas.

## Pontuação / pipeline
- [ ] `grade.py --validate` OK (V). Nomes únicos, `[Npt]` no nome = `points`.
- [ ] Cada `run` seleciona um grupo e realmente executa testes (um seletor errado que roda 0 testes pode passar!). Confirme no gabarito que cada entrada roda ≥ 1 teste, e no starter que reprova.
- [ ] Timeouts com folga para CI frio (download de dependências na 1ª execução).
- [ ] Workflow usa a mesma versão de runtime do manifesto.
- [ ] Integridade (gate `required`) cobre testes, fixtures e `.github/`.

## Higiene do repo
- [ ] `.gitignore` da stack; nada de `target/`, `node_modules/`, `.idea/`, relatórios.
- [ ] `.gitattributes` com `eol=lf` para scripts shell/wrappers (senão quebram no CI Linux quando criados no Windows).
- [ ] Wrappers executáveis (`git update-index --chmod=+x mvnw gradlew`).
- [ ] Commit inicial único ("Initial commit"), branch `main`.

## Anti-padrões encontrados nos exemplos (evitar)
- Seletor escapado de forma frágil: `-Dtest=\Classe\$Nested` — prefira `-Dtest='Classe$Nested'`.
- `mvn` no CI sem wrapper (depende da imagem) misturado com `./mvnw` em outros repos — padronize no wrapper.
- Fixture com nome duplicado de extensão (`invalid-observacao-null.json.json`).
- Datas fixas "futuras" que viram passado (`2026-12-01`) — o exercício expira.
- Starter já com classe de teste parcial que o aluno pode apagar sem penalidade (use integridade).
- Cobertura do projeto inteiro em vez do pacote alvo (DTOs/getters inflam o número).
