<h1> Library-api</h1>

<h3>Conexão com o banco MySQL:</h3>
O projeto conta com um arquivo chamado `banco.py` que é responável pela conexão com o banco de dados, nele temos alguns parâmetros que devem serem preenchidos:

`host` = {host de acesso ao banco} <br>
`user` = {usuário de acesso} <br>
`passwd` = {senha do usuário} <br>
`db` = {nome do banco}<br>
<br>
O restante das váriaveis do banco podem serem mantidas. <br>
Estarei anexando ao projeto também os scripts sql, para a criação do banco e das tabelas.
<br>
###Criação de Ambientes Virtuais
Navegue até o diretório do projeto e execute os comandos no terminal: <br>
<br>
Vamos instalar o pyenv para evitar que haja problemas de versionamento do python:<br>
`$ pip install pyenv-win` ou `$ pip install pyenv` em sistemas Linux.
<br>
Como utilizei o Python 3.7.8 para o desenvolvimento, rodaremos:<br>
`$ pyenv local 3.7.8`<br>

Após isso executaremos o comando para a criação da venv:<br>
`$ python -m venv myvenv`<br>

Ativando a venv:<br>
`$ source myvenv/bin/activate`

<h3>Instalando o `requeriments.txt`</h3>
Após ativar seu Ambiente virtual basta rodar o seguinte comando dentro do diretório:<br>
`pip install -r requirements.txt`<br><br>
Assim todas as bibliotecas e frameworks usadas(os) no projeto estarão no seu ambiente virtual.

<h2>Documentação da API</h2>

<h3>Endpoints:</h3>
`/client/{id_cliente}` 
retorna um cliente específico - Método `GET`<br>
`/client` 
retorna todos os clientes - Método `GET`<br>
`/books` 
retorna todos os livros - Método `GET`<br>
`/client/{id_cliente}/books`  retorna todos os livros reservados pelo cliente - Método `GET`<br><br>
`/books/{id_livro}/reserve`  Faz a reserva do livro especificado, necessitando de um body `JSON` com o `id_client` - Método `POST`<br>
exemplo: 
`{"id_client": {id do cliente}}`
<br><br>
`/reserve/{id da reserva}` 
deleta uma reserva feita - Método `DELETE`<br><br>
`/books`
insere livros no banco, passando uma lista com os seguintes campos: - Método `POST`<br>
exemplo de lista:<br>

`[{"title": "O Senhor dos Anéis",
   "autor": "J. R. R. Tolkien",
   "year_published": 1954,
   "price_location": 15},
   {"title": "Harry Potter e a Pedra Filosofal",
   "autor": "J. K. Rowling",
   "year_published": 1997,
   "price_location": 7},
   {"title": "Assassins Creed - Renascença",
   "autor": "Anton Gill",
   "year_published": 2009,
   "price_location": 20}]`
   <br><br>
`/client`  insere clientes no banco, recebendo em JSON uma lista com nome dos clientes - Método `POST`<br>
exemplo:<br>

`[{"name": "Matheus"},{"name": "João"},{"name": "Nathália"},{"name": "Igor"},]`<br><br>

   
   
