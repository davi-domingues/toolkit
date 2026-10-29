# Seleção das habilidades mais valiosas

Objetivo: dizer quais N habilidades (padrão 3) mais pesam para esta vaga, entre as da lista recebida.

## Método

1. **Leia a vaga e marque o que ela pede.** Separe o que é obrigatório, desejável e o desafio central (o problema que a pessoa contratada vai resolver). Se a descrição trouxer tecnologias e responsabilidades, o desafio central é a responsabilidade que mais se repete.
2. **Pontue cada habilidade da lista** em duas dimensões, de 0 a 3:
   - **Peso na vaga:** 3 se está no desafio central ou é obrigatória; 2 se é desejável ou aparece em mais de um trecho; 1 se é citada de passagem; 0 se não aparece.
   - **Sustentação do candidato:** 3 se o `profile.md` mostra uso real com resultado; 2 se há uso real sem resultado claro; 1 se é estudo ou contato curto; 0 se não há evidência.
3. **Ordene por peso x sustentação.** Desempate pelo peso na vaga.
4. **Evite redundância.** Se duas habilidades dizem a mesma coisa para a vaga (por exemplo, uma tecnologia e o conceito que ela implementa), fique com a mais específica e use a vaga aberta para uma de natureza diferente.
5. **Habilidade com peso alto e sustentação 0** não entra na lista; vira nota de lacuna fora do bloco, com a sugestão de como o candidato pode abordá-la.

## Sem `profile.md`

Pergunte ao usuário quais itens da lista ele realmente já usou e em que contexto. Não pontue sustentação por suposição.

## Saída

Lista numerada com a habilidade e uma linha explicando o vínculo com a vaga. Se a pontuação for apertada entre duas, diga qual ficou de fora e por quê.
