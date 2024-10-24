import pymysql
from app import app
from config_db import db_config
from flask import jsonify, request
import logging

logging.basicConfig(level=logging.ERROR)

def get_db_connection():
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['db'],
        cursorclass=pymysql.cursors.DictCursor
    )

def validate_customer_data(data, required_fields):
    return all(data.get(field) for field in required_fields)

# Create
@app.route('/cadastrar', methods=['POST'])
def create_customer():
    try:
        _json = request.json
        required_fields = ['nome_cliente', 'email_cliente', 'telefone_cliente', 'endereco_cliente', 'idade_cliente', 'cpf_cliente']
        
        if validate_customer_data(_json, required_fields) and request.method == 'POST':
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    sqlQuery = """
                    INSERT INTO cliente(
                        nome_cliente, email_cliente, telefone_cliente, 
                        endereco_cliente, idade_cliente, cpf_cliente) 
                    VALUES(%s, %s, %s, %s, %s, %s)
                    """
                    bindData = (_json['nome_cliente'], _json['email_cliente'], _json['telefone_cliente'], 
                                _json['endereco_cliente'], _json['idade_cliente'], _json['cpf_cliente'])
                    cursor.execute(sqlQuery, bindData)
                    conn.commit()
                    response = jsonify({'message': 'Cliente inserido com sucesso!'})
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
                cursor.execute("SELECT * FROM cliente")
                customerRows = cursor.fetchall()
                resp = jsonify(customerRows)
                resp.status_code = 200
                return resp
    
    except pymysql.MySQLError as e:
        logging.error(f"Erro no banco de dados: {e}")
        return jsonify({'error': 'Erro ao acessar o banco de dados.'}), 500
    except Exception as e:
        logging.error(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

# Read one
@app.route('/buscar/<string:nome_cliente>', methods=['GET'])
def customer_details(nome_cliente):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id_cliente, nome_cliente, email_cliente, telefone_cliente, 
                           endereco_cliente, idade_cliente, cpf_cliente
                    FROM cliente 
                    WHERE nome_cliente = %s
                """, (nome_cliente,))
                customerRow = cursor.fetchone()

                if not customerRow:
                    return jsonify({'error': 'Cliente não encontrado'}), 404
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
        required_fields = ['id_cliente', 'nome_cliente', 'email_cliente', 'telefone_cliente', 'endereco_cliente', 'idade_cliente', 'cpf_cliente']
        
        if validate_customer_data(_json, required_fields) and request.method == 'PUT':
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    sqlQuery = """
                        UPDATE cliente 
                        SET nome_cliente=%s, email_cliente=%s, telefone_cliente=%s, 
                        endereco_cliente=%s, idade_cliente=%s, cpf_cliente=%s 
                        WHERE id_cliente=%s
                    """
                    bindData = (_json['nome_cliente'], _json['email_cliente'], _json['telefone_cliente'], 
                                _json['endereco_cliente'], _json['idade_cliente'], _json['cpf_cliente'],
                                _json['id_cliente'])
                    cursor.execute(sqlQuery, bindData)
                    conn.commit()
                    response = jsonify('Informações do cliente atualizadas!')
                    response.status_code = 200
                    return response
        else:
            return jsonify({'error': 'Dados invalidos ou incompletos'}), 400

    except pymysql.MySQLError as e:
        logging.error(f"Erro no banco de dados: {e}")
        return jsonify({'error': 'Erro ao acessar o banco de dados.'}), 500
    except Exception as e:
        logging.error(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

# Delete
@app.route('/remover/<string:nome_cliente>', methods=['DELETE'])
def delete_customer(nome_cliente):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cliente WHERE nome_cliente=%s", (nome_cliente,))
                conn.commit()
                response = jsonify('Informações do cliente apagadas com sucesso!')
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
        'message': 'Cliente não encontrado: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run()
