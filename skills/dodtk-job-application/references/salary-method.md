# Pretensão salarial

Objetivo: propor e redigir uma pretensão salarial coerente com a vaga, o nível do candidato e o regime de contratação, ancorada em dados de mercado atuais e não em números de memória.

## 1. Entenda a pergunta

Extraia do formulário e da vaga:

- **Regime:** CLT, PJ, cooperado, outro.
- **Carga horária:** semanal (por exemplo 30h) e a referência de mercado para o cargo (normalmente 40h).
- **Modelo de trabalho:** presencial, híbrido, remoto.
- **Senioridade e escopo do cargo.**
- **Benefícios informados** pela empresa.
- **Formato da resposta:** valor único, faixa ou texto livre, e o limite de caracteres.

Se algo disso não estiver na vaga, pergunte ou declare a suposição na resposta ao usuário.

## 2. Pesquise o mercado

Dado salarial muda com o tempo, a região e o regime. Não use número de memória.

Quando houver ferramenta de busca na internet, pesquise antes de propor faixa:

- Faixa para o **cargo e senioridade** da vaga, na **região** ou no modelo remoto equivalente.
- Pelo menos **duas fontes independentes**, entre guias salariais de consultorias de recrutamento, sites de salários e vagas com faixa divulgada. Prefira fontes com data recente.
- Se a empresa for conhecida, veja o que ela divulga ou o que consta para o cargo.
- Anote fonte, data e se o valor é CLT ou PJ, 40h ou outra carga.

Se não houver busca disponível, peça ao usuário uma faixa que ele tenha encontrado e marque o resultado como estimativa.

## 3. Normalize para a mesma base

Compare tudo em **valor mensal bruto, mesmo regime e mesma carga**.

**CLT para PJ.** O valor PJ cobre o que o CLT dá como direitos: 13º (1/12 ao mês), férias com 1/3 (cerca de 1/9 ao mês), FGTS (8% do salário), benefícios (vale-refeição, saúde, outros) e a falta de remuneração em período sem contrato. Soma-se a isso o custo da empresa PJ (impostos conforme o regime tributário, contador). Por isso o PJ equivalente costuma ser maior que o CLT bruto. Confira alíquotas e limites vigentes na internet antes de usar números, pois mudam.

**Carga reduzida.** Se a faixa de mercado é para 40h e a vaga é de 30h, proporcional puro é `faixa x 30 / 40`. É um ponto de partida, não regra: empresas pagam proporcional, pagam cheio ou negociam no meio. Avise ao usuário que existe espaço para pedir acima do proporcional quando o escopo for o do cargo completo.

**Benefícios.** Compare remuneração total. Em CLT, benefícios entram na conta; em PJ, normalmente não.

## 4. Posicione a faixa

1. Separe a faixa de mercado para a senioridade do candidato (piso, mediana, teto).
2. Considere o nível real do candidato e a transição de carreira. Quem está mudando de nível costuma pedir entre o piso e a mediana da nova faixa.
3. Ajuste por escopo, modelo de trabalho (presencial costuma ter custos extras de deslocamento) e por quanto a vaga pede acima do nível.
4. Formule uma **faixa com amplitude moderada**, de modo que o piso seja um valor que o candidato aceitaria de fato.
5. Use **faixa**, não valor único, salvo se o formulário exigir um número.

## 5. Remuneração atual

Não cite o salário atual do candidato na resposta, a menos que o `salary.md` indique que ele quer fazer isso ou o formulário peça explicitamente. A pretensão se ancora no mercado, no escopo e na entrega, não no que ele ganha hoje. Use o salário atual apenas como piso interno de decisão: nunca proponha faixa cujo piso esteja abaixo do que o candidato aceitaria perder.

## 6. Respostas anteriores

Se o `salary.md` tiver respostas anteriores, trate-as como referência de tom e de formato, não como número a reaproveitar. Mercado, regime e carga mudaram; recalcule. Se a faixa nova divergir bastante da anterior, diga isso ao usuário e explique por quê.

## 7. Redação

- Mesmo estilo do `writing-style.md`.
- Estrutura: faixa, o que ela considera (escopo, nível, regime e carga), abertura para conversar.
- Linguagem de quem negocia com segurança, sem pedir desculpas e sem ultimato.
- Dentro do limite de caracteres e conforme [output-rules.md](output-rules.md).

## 8. Entrega ao usuário

Fora do bloco de texto, resuma em poucas linhas:

- Faixa de mercado encontrada, com fontes e datas.
- A conta de normalização que você fez (regime, carga).
- Faixa proposta e por que ela está nesse ponto.
- O que o usuário deve confirmar antes de enviar.
