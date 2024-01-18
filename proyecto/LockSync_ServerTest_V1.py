import time
import hashlib
import random
from flask import Flask, request, jsonify, send_from_directory

# Configuración del servidor Flask
app = Flask(__name__, static_folder='.')

# Almacena los códigos de acceso únicos
unique_codes = {}

# Almacena los usuarios autorizados con hashes de contraseñas
authorized_users = {
    "admin": hashlib.sha256("admin".encode()).hexdigest(),
    "user1": hashlib.sha256("user1".encode()).hexdigest()
}

# Almacena los tokens generados
valid_tokens = {}

# Estado de la puerta (simulado)
door_state = {"locked": True, "open": False}

# Genera un código único
def generate_unique_code():
    unique_code = str(random.randint(100000, 999999))
    unique_codes[unique_code] = time.time() + 300  # Código expira en 5 minutos
    return unique_code

# Genera un token de sesión
def generate_token():
    token = hashlib.sha256(str(time.time()).encode()).hexdigest()
    valid_tokens[token] = time.time() + 300  # Token expira en 5 minutos
    return token

# Verifica los códigos únicos
def check_unique_code(code):
    if code in unique_codes and time.time() < unique_codes[code]:
        return True
    return False

# Verifica las credenciales del usuario
def check_user_credentials(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return username in authorized_users and authorized_users[username] == hashed_password

# Rutas Flask
@app.route('/')
def index():
    return send_from_directory('.', 'index_rasp.html')

@app.route('/generate_code', methods=['POST'])
def generate_code():
    code = generate_unique_code()
    return jsonify({"code": code})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if check_user_credentials(username, password):
        token = generate_token()
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/door_status', methods=['GET'])
def get_door_status():
    return jsonify(door_state)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3080)
