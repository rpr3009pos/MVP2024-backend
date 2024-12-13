from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Configurações do Swagger 
SWAGGER_URL = '/swagger' 
API_URL = '/static/swagger.json' 
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "API de Clientes"}) 
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def init_db():
    conn = sqlite3.connect('clientes.db')
    conn.execute('PRAGMA journal_mode=WAL')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            dt_nasc TEXT NOT NULL,
            logradouro TEXT NOT NULL,
            cep TEXT NOT NULL,
            cidade TEXT NOT NULL,
            uf TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def conectar_db():
    conn = sqlite3.connect('clientes.db')
    conn.row_factory = sqlite3.Row
    return conn

def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)
    
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    
    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_digito = (soma * 10 % 11) % 10
    
    # Calcula o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_digito = (soma * 10 % 11) % 10
    
    # Verifica se os dígitos calculados são iguais aos do CPF fornecido
    return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"

@app.route("/")
def home():
    return " <!doctype html> <title>message</title> <h1>Flask está funcionando corretamente!!</h1> <p>parabéns!!!</p>    Isto é apenas um teste"

@app.route("/listar_clientes", methods=["GET"])
def listar_clientes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    clientes_list = [dict(cliente) for cliente in clientes]
    return jsonify(clientes_list)

@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():
    try:
        data = request.get_json()
        
        # Validação do CPF
        if not validar_cpf(data["cpf"]):
            return jsonify({"error": "CPF inválido!"}), 400
        
        conn = conectar_db()
        cursor = conn.cursor()
        
        # Verificar se o CPF já existe no banco de dados
        cursor.execute("SELECT * FROM clientes WHERE cpf = ?", (data["cpf"],))
        if cursor.fetchone():
            return jsonify({"error": "CPF ja cadastrado!"}), 400
        
        cursor.execute('''
            INSERT INTO clientes (nome, cpf, dt_nasc, logradouro, cep, cidade, uf)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data["nome"], data["cpf"], data["dt_nasc"], data["logradouro"],
              data["cep"], data["cidade"], data["uf"]))
        
        conn.commit()
        return jsonify({"message": "Cliente cadastrado com sucesso!"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if conn:
            conn.close()

@app.route("/editar_cliente/<id>", methods=["PUT"])
def editar_cliente(id):
    try:
        data = request.get_json()
        
        # Validação do CPF
        if not validar_cpf(data["cpf"]):
            return jsonify({"error": "CPF inválido!"}), 400
        
        conn = conectar_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE clientes
            SET nome = ?, cpf = ?, dt_nasc = ?, logradouro = ?, cep = ?, cidade = ?, uf = ?
            WHERE id = ?
        ''', (data["nome"], data["cpf"], data["dt_nasc"], data["logradouro"],
              data["cep"], data["cidade"], data["uf"], id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Cliente atualizado com sucesso!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/deletar_cliente/<int:id>", methods=["DELETE"])
def deletar_cliente(id):
    conn = None
    cursor = None
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        print(f"Deletando cliente com ID: {id}")  # Log para depuração
        cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Cliente não encontrado"}), 404
        conn.commit()
        return jsonify({"message": "Cliente removido com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# Listar todas as rotas registradas no Flask
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.methods} -> {rule}")

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)
