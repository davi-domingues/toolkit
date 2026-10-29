# Adaptação ao estilo de escrita

O estilo não é fixo na skill. Ele nasce dos textos do próprio usuário e se corrige com o uso. O resultado fica em `writing-style.md`, fora do repositório.

## Fontes, da mais forte para a mais fraca

1. **Textos reais do usuário** em `samples/` (apresentações, respostas de formulário, e-mails profissionais, posts, mensagens longas). Três a cinco textos curtos bastam.
2. **Correções do usuário** sobre textos gerados por esta skill: o que ele trocou, cortou ou reescreveu é o sinal mais confiável.
3. **Respostas a perguntas rápidas** quando não houver texto nenhum.

## Extraindo o estilo

Leia os textos e descreva, com exemplos curtos e sem copiar trechos longos:

- **Pessoa e distância:** primeira pessoa, formal ou próximo, uso de "você", "eu", "a gente".
- **Ritmo:** tamanho médio das frases, uso de frases curtas para ênfase, parágrafos longos ou curtos.
- **Vocabulário:** termos técnicos em inglês ou traduzidos, nível de formalidade, expressões que a pessoa repete.
- **Abertura e fecho:** como costuma começar e terminar.
- **Pontuação:** vírgulas, ponto e vírgula, travessão, reticências, exclamação.
- **Tom:** humildade, confiança, entusiasmo, objetividade, humor.
- **O que a pessoa evita:** clichês, superlativos, jargão corporativo.

Registre como **regras observáveis** ("frases de até 20 palavras", "abre com o contexto, não com o nome"), não como adjetivos soltos.

## Sem nenhum texto

Faça no máximo cinco perguntas curtas, uma rodada só:

1. Prefere um tom mais direto ou mais caloroso?
2. Costuma escrever frases curtas ou mais elaboradas?
3. Usa termos técnicos em inglês ou prefere traduzir?
4. Algum jeito de começar ou terminar um texto que você gosta ou detesta?
5. Quer soar mais humilde ou mais confiante?

Gere o `writing-style.md` com o campo `status: provisório` e avise o usuário. Peça que cole um texto dele depois, para refinar.

## Refinando com o uso

Quando o usuário editar uma resposta gerada:

1. Compare a versão dele com a sua. Liste as diferenças que se repetem.
2. Proponha atualizar `writing-style.md` com a regra nova. Só grave com confirmação.
3. Troque `status: provisório` por `status: calibrado` após duas ou mais rodadas sem grandes ajustes.

## Adaptação por contexto

O estilo base pode variar conforme o canal. Mantenha em `writing-style.md` uma seção por contexto quando o usuário mostrar diferença real (formulário, carta, mensagem a recrutador). Na dúvida, use o estilo base.

## Limites

- Imitar a voz não é licença para inventar fato. O conteúdo vem do perfil.
- Texto em `samples/` é privado: não repita trechos dele em respostas nem em logs.
