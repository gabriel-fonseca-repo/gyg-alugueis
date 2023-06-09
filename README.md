# Gyg Alugueis!

## Site simples e prático para alugueis de automóveis.

Desenvolvido em Python com as tecnologias Flask e PostgreSQL.

## Inicialização do projeto:

1. Explicitar as variáveis de ambiente do banco de dados no arquivo `.env` na raiz do projeto:
   1. `DB_USER_NAME` > nome do usuário do banco.
   2. `DB_USER_PSWD` > senha do usuário do banco.
   3. `DB_HOST` > endereço (URI) do host do banco de dados.
   4. `DB_NAME` > nome do banco.
   5. `DB_DRIVER` > driver do banco que será utilizado.
   6. `SCRKEY` > chave secreta da aplicação.
   7. Vale lembrar que há um arquivo `.env` vazio na raiz do projeto com o nome `.env.example` que serve apenas para ser copiado, preenchido e renomeado para `.env` para que funcione normalmente.
2. Instalar as dependências: `pip install -r requirements.txt`.
3. Rodar as migrations para sincronização com o banco:
   1. Caso seja a primeira vez inicializando, rodar o seguinte comando para gerar os arquivos de migração: `python -m flask db init`.
   2. Rodar o comando `python -m flask db migrate` para gerar os arquivos de migração.
   3. E finalmente o comando `python -m flask db upgrade` para executar o DDL gerado pela migrations e sincronizar o banco.

## Observações e erros conhecidos:

1. Erro de sincronização do banco: `ERROR [flask_migrate] Error: Target database is not up to date.` é atirado quando o banco de dados não está sincronizado com o ORM. Executar os seguintes comandos:
   1. O comando `python -m flask db stamp head` irá adicionar uma tabela `alembic_version` no banco e começar a acompanhar as mudanças do mesmo, trazendo novamente a sincronização.
   2. Após o primeiro passo, basta continuar a atualização do banco normalmente, com os comandos `python -m flask db migrate` e `python -m flask db upgrade`.

## Desenvolvedores:

- (⌐■_■) - [Gabriel R.](https://github.com/gabriel-fonseca-repo)
- ╰(\*°▽°\*)╯ - [Yasmim S.](https://github.com/ysrod)
- (\*/ω＼\*) - [Gabriel F.](https://github.com/H-Gabriel)
