from flask import Flask, jsonify, request
import datetime
import banco

conn, cur = banco.conecta_banco()
app = Flask(__name__)


# Busca geral de livros:
def busca_livros(id_book) -> list:
    sql_busca = """SELECT * FROM books """
    if id_book:
        sql_busca += f"WHERE idbook = {id_book} "
    cur.execute(sql_busca)
    results = cur.fetchall()
    return results


# Busca de reservas, passando o id ela retorna para cliente específico, caso contrário busca todas as reservas:
def busca_reservas(idcliente) -> list:
    sql_reservas = f"""SELECT * FROM reservas """
    if idcliente:
        sql_reservas += f"WHERE id_client = {idcliente} "

    cur.execute(sql_reservas)
    reservas = cur.fetchall()
    return reservas


# Função para verificar a disponibilidade do livro solicitado:
def verifica_status_livro(books) -> list:
    reservas = busca_reservas(idcliente=None)
    for livro in books:
        for reserva in reservas:
            if livro['idbook'] == reserva['id_book']:
                status = "Emprestado"
                break
            else:
                status = "Disponível"

        livro['status'] = status
    return books


# Busca geral de clientes:
def busca_clientes(idcliente) -> list:
    sql_busca = """SELECT * FROM clients """

    if idcliente:
        sql_busca += f"WHERE idclient = {idcliente}"
    cur.execute(sql_busca)
    results = cur.fetchall()
    return results


# Rota para um cliente:
@app.route('/client/<int:id>', methods=['GET'])
def client_one(id):
    clientes_ = busca_clientes(id)
    return jsonify(clientes_), 200


# Rota para total de clientes:
@app.route('/client', methods=['GET'])
def home():
    clientes_ = busca_clientes(None)
    return jsonify(clientes_), 200


# Rota para total de livros:
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(verifica_status_livro(busca_livros(None))), 200


# Rota para livros emprestados para um cliente: caso lista seja '1' o retorno é em lista, caso contrário em json.
@app.route('/client/<int:id>/books', methods=['GET'])
def client_books(id, list=0):
    reservas = busca_reservas(idcliente=id)
    for res in reservas:
        if id == res['id_client']:
            data_entrega = res['data_entrega']

            # TODO: AQUI É POSSÍVEL ALTERAR A DATA DO DIA DE PESQUISA:
            hoje = datetime.datetime.now()
            # hoje = datetime.datetime(year=2021, month=3, day=30)

            dias = abs((hoje - data_entrega).days)

            # verifica a situação da reserva e caso esteja atrasada calcula os custos:
            if data_entrega > hoje:
                situacao = "Em dia"
                res['situacao'] = situacao
            else:
                situacao = "Atrasado"
                for book in busca_livros(None):
                    if res['id_book'] == book['idbook']:
                        location_value = book['preco_locacao']
                        book_name = book['titulo']

                if dias >= 1 and dias <= 3:
                    multa = location_value * 0.03
                    juros = (location_value * 0.002) * dias
                    total = location_value + multa + juros

                if dias > 3 and dias <= 5:
                    multa = location_value * 0.05
                    juros = (location_value * 0.004) * dias
                    total = location_value + multa + juros

                if dias > 5:
                    multa = location_value * 0.07
                    juros = (location_value * 0.006) * dias
                    total = location_value + multa + juros

                res['valor_a_pagar'] = total
                res['book_title'] = book_name
            res['situacao'] = situacao
            res['data_entrega'] = datetime.datetime.strftime(res['data_entrega'], "%Y-%m-%dT%H:%M:%S")
            res['data_reserva'] = datetime.datetime.strftime(res['data_reserva'], "%Y-%m-%dT%H:%M:%S")

        else:
            return jsonify({'error': "cliente não encontrado", 'code': 404}), 404
    if list == 0:
        return jsonify(reservas), 200
    else:
        return reservas


# Rota para reservar um livro:
@app.route('/books/<int:id>/reserve', methods=['POST'])
def reserve(id):
    data = request.get_json()

    # verifica se o id do livro existe:
    controle = 0
    for book in busca_livros(None):
        if id == book['idbook']:
            id_book = book['idbook']

            # Verifica se o livro está disponível para emprestimo:
            book = verifica_status_livro(busca_livros(id_book))
            if book[0]['status'] == "Emprestado":
                return jsonify({'error': 'livro já emprestado',
                                'code': 400}), 400
            else:
                controle = 1
    if controle == 0:
        return jsonify({'error': 'id_book not found',
                        'code': 400}), 404

    # verifica se o id do cliente existe:
    controle = 0
    if 'id_client' in data:
        for cliente in busca_clientes(None):
            if data['id_client'] == cliente['idclient']:
                idcliente = cliente['idclient']
                controle = 1
        if controle == 0:
            return jsonify({'error': 'id_client not found',
                            'code': 400}), 404
    else:
        return jsonify({'error': 'id_client not found',
                        'code': 400}), 404

    # Verifica se o cliente possui um pendência de reserva
    cli_books = client_books(idcliente, list=1)
    for cli_res in cli_books:
        if cli_res['situacao'] == "Atrasado":
            return jsonify({'info': 'Você possui uma reserva atrasada',
                            'code': 200, 'id_reserva': cli_res['idreserva']}), 201

    data_reserva = datetime.datetime.now()
    data_entrega = data_reserva + datetime.timedelta(days=3)

    insert_reserva = f"""INSERT INTO reservas (data_reserva, data_entrega, id_book, id_client)
                        VALUES ('{data_reserva}', '{data_entrega}', {id_book}, {idcliente})"""

    cur.execute(insert_reserva)
    conn.commit()

    return jsonify({'info': 'reserva feita com sucesso',
                    'code': 200}), 201


# Rota para deletar uma reserva
@app.route('/reserve/<int:idreserva>', methods=['DELETE'])
def remove_reserve(idreserva):
    try:
        sql_delete_reserve = f"""DELETE FROM reservas WHERE idreserva = {idreserva}"""
        cur.execute(sql_delete_reserve)
        conn.commit()
        return jsonify({'message': 'reserva deletada com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': 'falha ao deletar a reserva', 'msg': e}), 400


# Rota para cadastrar livros
@app.route('/books', methods=['POST'])
def cadastro_books():
    data = request.get_json()
    for livro in data:
        titulo = livro['title']
        autor = livro['author']
        ano_publicacao = livro['year_published']
        preco_locacao = livro['price_location']

        try:
            sql_insert_book = f"""INSERT INTO books (titulo, autor,ano_publicacao, preco_locacao)
                            VALUES ('{titulo}', '{autor}', '{ano_publicacao}', {preco_locacao})
                            ON DUPLICATE KEY UPDATE titulo = '{titulo}'"""
            cur.execute(sql_insert_book)
            conn.commit()
        except Exception as e:
            return jsonify({'error': 'Livros Não Inseridos', 'desc': e}), 500
    return jsonify({'msg': 'Livros Inseridos'}), 200


# Rota para cadastrar clientes
@app.route('/client', methods=['POST'])
def cadastro_client():
    data = request.get_json()
    for client in data:
        nome = client['name']

        try:
            sql_insert_client = f"""INSERT INTO clients (nome)
                            VALUES ('{nome}')"""
            cur.execute(sql_insert_client)
            conn.commit()
        except Exception as e:
            return jsonify({'error': 'Clientes Não Inseridos', 'desc': e}), 500
    return jsonify({'msg': 'Clientes Inseridos'}), 200


if __name__ == '__main__':
    app.run(debug=True)
