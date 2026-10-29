---
name: dodtk-job-application
description: Ajuda a responder candidaturas a vagas de emprego a partir de qualquer descrição de vaga, lista de habilidades e cenário do candidato. Seleciona as habilidades mais valiosas para a vaga, escreve apresentação pessoal com limite de caracteres no estilo de escrita do usuário e define pretensão salarial (CLT, PJ, carga horária reduzida) com dados de mercado pesquisados. Use quando o usuário colar uma vaga, pedir "me ajuda a me candidatar", "escreve minha apresentação", "qual pretensão salarial" ou responder formulário de processo seletivo. Perfil, estilo de escrita e cenário salarial ficam fora do repositório e são criados e mantidos por esta skill.
---

# Candidatura a vagas

Produz respostas de candidatura sob medida para cada vaga, sem dados pessoais dentro do repositório. Tudo o que é do usuário vive em uma pasta própria fora do repo; a skill só traz o método e os templates.

## Regras que não mudam

1. Nunca grave dado pessoal (perfil, salário, benefícios, textos do usuário) dentro do repositório do toolkit nem em commit, PR ou log.
2. Nunca afirme experiência, tecnologia, cargo ou resultado que não esteja no perfil ou na conversa. Na dúvida, pergunte.
3. Nunca invente dado de mercado. Pesquise na internet quando a ferramenta existir; sem ela, peça a faixa ao usuário e marque o valor como estimativa.
4. Respeite o limite de caracteres de cada resposta e confira a contagem antes de entregar.
5. Entregue texto final em bloco único copiável e sem formatação, conforme [references/output-rules.md](references/output-rules.md).

## Dados do usuário (fora do repo)

Pasta padrão: `~/.dod-toolkit/job-application/`. A variável de ambiente `DODTK_JOB_HOME` sobrescreve o caminho.

| Arquivo | Conteúdo | Template |
|---|---|---|
| `profile.md` | trajetória, habilidades, projetos, objetivos | [templates/profile.template.md](templates/profile.template.md) |
| `writing-style.md` | como o usuário escreve | [templates/writing-style.template.md](templates/writing-style.template.md) |
| `salary.md` | cenário atual, preferências e respostas anteriores sobre salário | [templates/salary.template.md](templates/salary.template.md) |
| `samples/` | textos reais do usuário, usados só para extrair o estilo | |

No início de toda execução:

1. Resolva o caminho e veja quais arquivos existem.
2. Se faltar algum que o modo escolhido exige, siga [references/setup-and-maintenance.md](references/setup-and-maintenance.md) para criá-lo a partir do template, conversando com o usuário.
3. Se o caminho estiver dentro de um repositório git, avise e peça outro local.
4. Ao final, se o usuário corrigiu seu texto ou trouxe dado novo, proponha atualizar os arquivos e só grave com confirmação.

## Inputs

Nada é fixo. Receba, nesta ordem de prioridade, o que o usuário colar ou apontar; o que faltar vem dos arquivos, e o que ainda faltar você pergunta.

| Input | Obrigatório em | Se faltar |
|---|---|---|
| `vaga` (descrição) | habilidades, apresentação, salário | pergunte; nunca deduza a vaga |
| `habilidades` (lista) | habilidades | use as do `profile.md`; se vazio, extraia da vaga |
| `cenario` (nível, regime, remuneração) | salário | use `salary.md`; se vazio, pergunte |
| `pergunta` (texto do formulário) | salário | assuma a pergunta padrão de pretensão e avise |
| `modo` | sempre | `tudo` se o pedido cobrir mais de um; senão o que foi pedido |
| `limite` (caracteres) | apresentação, salário | 1500 e 1000; use o que o formulário informar |

Sem descrição de vaga (vazia ou só aspas), pare e peça o texto antes de gerar qualquer coisa.

## Modos

### habilidades

Escolhe as N habilidades mais valiosas para a vaga (padrão 3). Método em [references/skills-selection.md](references/skills-selection.md). Entregue as escolhidas com uma linha de justificativa cada.

### apresentacao

Escreve a apresentação pessoal. Método em [references/presentation.md](references/presentation.md). Use o estilo de `writing-style.md`; sem ele, siga [references/style-adaptation.md](references/style-adaptation.md) para criar um provisório.

### salario

Define e redige a pretensão salarial. Método em [references/salary-method.md](references/salary-method.md). Pesquise dados de mercado atuais antes de propor faixa.

### tudo

Executa habilidades, apresentação e salário, nessa ordem, reaproveitando a leitura da vaga.

## Fechamento

Depois de entregar, pergunte em uma frase se quer ajustar tom, tamanho ou ênfase. Use o retorno para manter os arquivos do usuário atualizados.
