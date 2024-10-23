import pymysql
from app import app
from config_db import db_config
import pymysql

from flask import jsonify, request

#create
@app.route('/cadastar', methods=['POST'])
def create_customer():
    try:
        _json = request.json
        _name = _json['nome_produto']
        _barcode = _json['cod_barras_produto']
        _manufacturer = _json['fabricante_produto']
        _manDate = _json['data_fabircacao_produto']
        _expiration = _json['data_validade_produto']
        _category = _json['categoria_produto']
        _weight = _json['peso_produto']
        _price = _json['preco_produto']

        if _name and _barcode and _manufacturer and _manDate and _expiration and _category and _weight and _price and request.method == 'POST':
            conn = pymysql.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                db=db_config['db'],
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()
            sqlQuery = """INSERT INTO produtos(nome_produto, cod_barras_produto, fabricante_produto, 
                data_fabircacao_produto, data_validade_produto, categoria_produto, peso_produto, preco_produto) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
            bindData = (_name, _barcode, _manufacturer, _manDate, _expiration, _category, _weight, _price)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify({'message': 'Produto inserido com sucesso!'})
            response.status_code = 201
            return response
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
@app.route('/buscar', methods=['GET'])
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
        cursor.execute("SELECT * FROM produtos")
        customerRows = cursor.fetchall()
        response = jsonify(customerRows)
        response.status_code = 200
        return response
    
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

#read one
@app.route('/buscar/<string:nome_produto>', methods=['GET'])
def customer_details(nome_produto):
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
            SELECT nome_produto, cod_barras_produto, fabricante_produto, 
            data_fabircacao_produto, data_validade_produto, categoria_produto, peso_produto, preco_produto 
            FROM produtos 
            WHERE nome_produto = %s
        """, (nome_produto,))
        customerRow = cursor.fetchone()
        if not customerRow:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        response = jsonify(customerRow)
        response.status_code = 200
        return response

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#update
@app.route('/atualizar', methods=['PUT'])
def update_customer():
    conn = None
    cursor = None
    try:
        _json = request.json
        _id = _json['id_produto']
        _name = _json['nome_produto']
        _barcode = _json['cod_barras_produto']
        _manufacturer = _json['fabricante_produto']
        _manDate = _json['data_fabircacao_produto']
        _expiration = _json['data_validade_produto']
        _category = _json['categoria_produto']
        _weight = _json['peso_produto']
        _price = _json['preco_produto']
        
        if _name and _barcode and _manufacturer and _manDate and _expiration and _category and _weight and _price and _id and request.method == 'POST':
            conn = pymysql.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                db=db_config['db'],
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = conn.cursor()
            sqlQuery = """
                UPDATE produtos 
                SET nome_produto=%s, cod_barras_produto=%s, fabricante_produto=%s, data_fabircacao_produto=%s,
                data_validade_produto=%s, categoria_produto=%s, peso_produto=%s, preco_produto=%s
                WHERE id_produto=%s
            """
            bindData = (_name, _barcode, _manufacturer, _manDate, _expiration, _category, _weight, _price, _id)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Informações do produto atualizadas!')
            response.status_code = 200
            return response
        else:
            return jsonify({'error': 'Dados invalidos ou incompletos'}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#delete
@app.route('/remover/<string:nome_produto>', methods=['DELETE'])
def delete_customer(nome_produto):
    try:
        conn = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            db=db_config['db'],
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE nome=%s", (nome_produto,))
        conn.commit()
        response = jsonify('Informações do produtos removidas com sucesso!')
        response.status_code = 200
        return response

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
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run()