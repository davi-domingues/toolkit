# Criar e manter os arquivos do usuário

Os arquivos do usuário ficam fora do repositório do toolkit, em `~/.dod-toolkit/job-application/` (ou no caminho de `DODTK_JOB_HOME`). Esta skill cria, atualiza e nunca versiona esses arquivos.

## Resolver o caminho

1. Se `DODTK_JOB_HOME` estiver definida, use-a.
2. Senão, use `~/.dod-toolkit/job-application/`.
3. Se o diretório estiver dentro de um repositório git (existe `.git` em algum pai), avise o usuário e peça outro local. Dado pessoal não pode ir para um repo.
4. Crie o diretório e a subpasta `samples/` quando o usuário confirmar.

## Criar a partir do template

Para cada arquivo que o modo escolhido exige e não existe:

1. Leia o template em `templates/`.
2. Conduza uma conversa curta, uma seção por vez, preenchendo os campos com as respostas do usuário. Aceite que ele cole um currículo, um perfil profissional ou um texto livre e extraia dali o que for possível; mostre o resultado e peça confirmação.
3. Campo que o usuário não quer preencher fica vazio. Nunca preencha por suposição.
4. Grave o arquivo no caminho do usuário e confirme onde ficou.

Mínimo por modo:

| Modo | Exige |
|---|---|
| habilidades | `profile.md` (seção de habilidades) |
| apresentacao | `profile.md` e `writing-style.md` (pode ser provisório) |
| salario | `salary.md` e `writing-style.md` (pode ser provisório) |

## Manter

Proponha atualização, sem gravar automaticamente, quando:

- o usuário trouxer fato novo (projeto, tecnologia, cargo, resultado);
- o cenário salarial mudar (novo regime, nova remuneração, nova meta);
- o usuário editar um texto gerado (sinal para o `writing-style.md`);
- a vaga mostrar uma lacuna recorrente que o perfil poderia cobrir.

Mostre o trecho que vai mudar e grave só após confirmação. Ao atualizar `salary.md`, acrescente a resposta enviada à seção de histórico, com data e contexto da vaga em uma linha.

## Higiene

- Os arquivos contêm dados pessoais. Não os cole em saídas, commits, PRs, issues nem logs.
- Ao citar algo do perfil em uma resposta, use só o necessário para a vaga.
- Se o usuário pedir para apagar tudo, remova apenas os arquivos desta pasta e confirme.
- Se o usuário quiser sincronizar entre máquinas, sugira um repositório privado dele ou um cofre de notas, nunca o repositório do toolkit.

## Novos templates

Se uma nova necessidade aparecer (por exemplo, perguntas frequentes de formulário, carta de apresentação, histórico de candidaturas):

1. Proponha o novo arquivo ao usuário e explique a utilidade.
2. Crie o template em `templates/` do repositório **sem nenhum dado real**, apenas campos com placeholders `<assim>`.
3. Crie a instância preenchida no caminho do usuário, nunca no repo.
