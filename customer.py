import pymysql
from app import app
from config_db import db_config 

from flask import jsonify, request

#create
@app.route('/cliente/cadastar', methods=['POST'])
def create_customer():
    try:
        _json = request.json
        _name = _json['nome_cliente']
        _surname = _json['sobrenome_cliente']
        _email = _json['email_cliente']
        _phone = _json['telefone_celular_cliente']
        _address = _json['endereco_cliente']
        _age = _json['idade_cliente']
        _cpf = _json['cpf_cliente']

        if _name and _surname and _email and _phone and _address and _age and _cpf and request.method == 'POST':
            conn = pymysql.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                db=db_config['db'],
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()
            sqlQuery = """INSERT INTO cliente(nome_cliente, sobrenome_cliente, email_cliente, 
                telefone_celular_cliente, endereco_cliente, idade_cliente, cpf_cliente) 
                VALUES(%s, %s, %s, %s, %s, %s, %s)"""
            bindData = (_name, _surname, _email, _phone, _address, _age, _cpf)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            resp = jsonify({'message': 'Cliente inserido com sucesso!'})
            resp.status_code = 201
            return resp
        else:
            return jsonify({'error': 'Dados incorretos'}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#read one
@app.route('/cliente/buscar', methods=['GET'])
def customer():
    try:
        conn = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            db=db_config['db'],
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente")
        customerRows = cursor.fetchall()
        resp = jsonify(customerRows)
        resp.status_code = 200
        return resp
    
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

#read one
@app.route('/cliente/buscar/<string:nome_cliente>', methods=['GET'])
def customer_details(nome_cliente):
    try:
        conn = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            db=db_config['db'],
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nome_cliente, sobrenome_cliente, email_cliente, telefone_celular_cliente, 
            endereco_cliente, idade_cliente, cpf_cliente 
            FROM cliente 
            WHERE nome_cliente = %s
        """, (nome_cliente,))
        customerRow = cursor.fetchone()
        if not customerRow:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        resp = jsonify(customerRow)
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#update
@app.route('cliente/atualizar', methods=['PUT'])
def update_customer():
    try:
        _json = request.json
        _name = _json['nome_cliente']
        _surename = _json['sobrenome_cliente']
        _email = _json['email_cliente']
        _phone = _json['telefone_celular_cliente']
        _address = _json['endereco_cliente']
        _age = _json['idade_cliente']
        _cpf = _json['cpf_cliente']
        
        if _name and _surename and _email and _phone and _address and _age and _cpf and request.method == 'PUT':
            conn = pymysql.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                db=db_config['db'],
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()
            sqlQuery = """
                UPDATE cliente SET sobrenome_cliente=%s, email_cliente=%s, telefone_celular_cliente=%s, 
                endereco_cliente=%s, idade_cliente=%s, cpf_cliente=%s 
                WHERE nome_cliente=%s
            """
            bindData = (_surename, _email, _phone, _address, _age, _cpf, _name)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            resp = jsonify('Informações do Cliente atualizadas!')
            resp.status_code = 200
            return resp
        else:
            return showMessage("Dados incompletos ou inválidos")

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#delete
@app.route('/cliente/apagar/<string:nome_cliente>', methods=['DELETE'])
def delete_customer(nome_cliente):
    try:
        conn = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            db=db_config['db'],
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cliente WHERE nome_cliente=%s", (nome_cliente,))
        conn.commit()
        resp = jsonify('Informações do cliente apagadas com sucesso!')
        resp.status_code = 200
        return resp

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Cliente não encontrado: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run()