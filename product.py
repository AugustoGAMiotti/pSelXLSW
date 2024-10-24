import pymysql
from app import app
from config_db import db_config
from flask import jsonify, request
import logging
from datetime import datetime

logging.basicConfig(level=logging.ERROR)

def get_db_connection():
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['db'],
        cursorclass=pymysql.cursors.DictCursor
    )

def validate_product_data(data, required_fields):
    return all(data.get(field) for field in required_fields)

# Create
@app.route('/cadastrar', methods=['POST'])
def create_customer():
    try:
        _json = request.json
        required_fields = ['nome_produto', 'cod_barras_produto', 'fabricante_produto', 
                           'data_validade_produto', 'categoria_produto', 'preco_produto']
        
        if validate_product_data(_json, required_fields) and request.method == 'POST':

            try:
                data_validade_produto = datetime.strptime(_json['data_validade_produto'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
            
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    sqlQuery = """
                    INSERT INTO produtos(
                            nome_produto, cod_barras_produto, fabricante_produto, 
                            data_validade_produto, categoria_produto, preco_produto) 
                        VALUES(%s, %s, %s, %s, %s, %s)
                    """
                    bindData = (_json['nome_produto'], _json['cod_barras_produto'], _json['fabricante_produto'], 
                                data_validade_produto, _json['categoria_produto'], _json['preco_produto'])
                    cursor.execute(sqlQuery, bindData)
                    conn.commit()
                    response = jsonify({'message': 'Produto inserido com sucesso!'})
                    response.status_code = 201
                    return response
        else:
            return jsonify({'error': 'Dados incorretos'}), 400

    except pymysql.MySQLError as e:
        logging.error(f"Erro no banco de dados: {e}")
        return jsonify({'error': 'Erro ao acessar o banco de dados.'}), 500
    except Exception as e:
        logging.error(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

# Read all
@app.route('/buscar', methods=['GET'])
def customer():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM produtos")
                customerRows = cursor.fetchall()
                response = jsonify(customerRows)
                response.status_code = 200
                return response
    
    except pymysql.MySQLError as e:
        logging.error(f"Erro no banco de dados: {e}")
        return jsonify({'error': 'Erro ao acessar o banco de dados.'}), 500
    except Exception as e:
        logging.error(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

# Read one
@app.route('/buscar/<string:nome_produto>', methods=['GET'])
def customer_details(nome_produto):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT nome_produto, cod_barras_produto, fabricante_produto, 
                           data_validade_produto, categoria_produto, preco_produto 
                    FROM produtos 
                    WHERE nome_produto = %s
                """, (nome_produto,))
                customerRow = cursor.fetchone()

                if not customerRow:
                    return jsonify({'error': 'Produto não encontrado'}), 404
                response = jsonify(customerRow)
                response.status_code = 200
                return response

    except pymysql.MySQLError as e:
        logging.error(f"Erro no banco de dados: {e}")
        return jsonify({'error': 'Erro ao acessar o banco de dados.'}), 500
    except Exception as e:
        logging.error(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

# Update
@app.route('/atualizar', methods=['PUT'])
def update_customer():
    try:
        _json = request.json
        required_fields = ['id_produto', 'nome_produto', 'fabricante_produto', 
                           'data_validade_produto', 'categoria_produto', 'preco_produto']
        
        if validate_product_data(_json, required_fields) and request.method == 'PUT':

            try:
                data_validade_produto = datetime.strptime(_json['data_validade_produto'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    sqlQuery = """
                        UPDATE produtos 
                        SET nome_produto=%s, cod_barras_produto=%s, fabricante_produto=%s, 
                        data_validade_produto=%s, categoria_produto=%s, preco_produto=%s
                        WHERE id_produto=%s
                    """
                    bindData = (_json['nome_produto'], _json['cod_barras_produto'], _json['fabricante_produto'], 
                                data_validade_produto, _json['categoria_produto'], _json['preco_produto'], 
                                _json['id_produto'])
                    cursor.execute(sqlQuery, bindData)
                    conn.commit()
                    response = jsonify('Informações do produto atualizadas!')
                    response.status_code = 200
                    return response
        else:
            return jsonify({'error': 'Dados inválidos ou incompletos'}), 400

    except pymysql.MySQLError as e:
        logging.error(f"Erro no banco de dados: {e}")
        return jsonify({'error': 'Erro ao acessar o banco de dados.'}), 500
    except Exception as e:
        logging.error(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

# Delete
@app.route('/remover/<string:nome_produto>', methods=['DELETE'])
def delete_customer(nome_produto):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM produtos WHERE nome_produto=%s", (nome_produto,))
                produto = cursor.fetchone()

                if not produto:
                    return jsonify({'error': 'Produto não encontrado'}), 404

                cursor.execute("DELETE FROM produtos WHERE nome_produto=%s", (nome_produto,))
                conn.commit()
                response = jsonify('Informações do produto removidas com sucesso!')
                response.status_code = 200
                return response

    except pymysql.MySQLError as e:
        logging.error(f"Erro no banco de dados: {e}")
        return jsonify({'error': 'Erro ao acessar o banco de dados.'}), 500
    except Exception as e:
        logging.error(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Produto não encontrado: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run()
