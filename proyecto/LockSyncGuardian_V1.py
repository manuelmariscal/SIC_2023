import threading
import time
from flask import Flask, request, jsonify, send_from_directory
import mfrc522
import hashlib
import random
from machine import Pin, I2C, SPI
import ssd1306
import keypad

app = Flask(__name__, static_folder='.')

# Configuración del lector RFID
sda_pin = 8
rst_pin = 25
spi = SPI(1, baudrate=100000, polarity=0, phase=0)
reader = mfrc522.MFRC522(spi=spi, sda=sda_pin, rst=rst_pin)

# Configuración de la pantalla OLED
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuración del teclado matricial
keypad_pins = [Pin(i, Pin.IN, Pin.PULL_UP) for i in [15, 2, 0, 4, 16, 17, 5, 18]]
key_map = ['1', '2', '3', 'A', '4', '5', '6', 'B', '7', '8', '9', 'C', '*', '0', '#', 'D']
kp = keypad.KeyMatrix(rows=keypad_pins[:4], cols=keypad_pins[4:], keys=key_map)


# Configuración del solenoide
solenoid_pin = 23  
solenoid = Pin(solenoid_pin, Pin.OUT)

# Configuración del sensor de estado de la puerta
door_sensor_pin = 24  
door_sensor = Pin(door_sensor_pin, Pin.IN)

# Configuración del sensor IR
ir_sensor_pin = 17
ir_sensor = Pin(ir_sensor_pin, Pin.IN)

# Almacena los UIDs RFID autorizados
authorized_rfid_uids = set()

# Flag para controlar el registro de nuevos UIDs
registration_mode = False

# Almacena los códigos de acceso únicos
unique_codes = {}

# Almacena los usuarios autorizados con hashes de contraseñas
authorized_users = {
    "admin": hashlib.sha256("admin".encode()).hexdigest(),
    "user1": hashlib.sha256("user1".encode()).hexdigest()
}

# Almacena los tokens generados
valid_tokens = {}

# Funciones de utilidad
def is_code_valid(code):
    return code in unique_codes and time.time() < unique_codes[code]

def display_message(message):
    oled.fill(0)
    oled.text(message, 0, 20)
    oled.show()

def read_rfid():
    try:
        (status, tag_type) = reader.request(reader.REQIDL)
        if status == reader.OK:
            (status, raw_uid) = reader.anticoll()
            if status == reader.OK:
                return "%02x%02x%02x%02x" % tuple(raw_uid)
    except Exception as e:
        print("Error reading RFID:", e)
    return None


# Función para controlar el solenoide
def control_solenoid(lock):
    if lock:
        solenoid.value(0)  # Bloquear la puerta
        door_state["locked"] = True
    else:
        solenoid.value(1)  # Desbloquear la puerta
        door_state["locked"] = False
    # Actualizar el estado de la puerta basado en el sensor
    door_state["open"] = door_sensor.value() == 1

# Función para el bucle de control de acceso
def access_control_loop():
    global door_state, registration_mode, authorized_rfid_uids
    code_entered = ""
    
    while True:
        # Revisar si el sistema está en modo de registro
        if registration_mode:
            uid = read_rfid()
            if uid:
                authorized_rfid_uids.add(uid)
                display_message(f"UID {uid} registrado")
                time.sleep(2)
                oled.fill(0)
            continue  # Continuar en el bucle para seguir en modo de registro

        # Funcionamiento normal (modo de acceso)
        key = kp.get_key()
        if key:
            oled.fill(0)
            oled.text("Tecla: " + key, 0, 0)
            oled.show()
            if key.isdigit() or key in ['A', 'B', 'C', 'D', '*']:
                code_entered += key
            if key == '#':
                if is_code_valid(code_entered):
                    display_message("Acceso Aprobado")
                    control_solenoid(False)  # Desbloquear
                else:
                    display_message("Acceso Denegado")
                    control_solenoid(True)  # Bloquear
                code_entered = ""
                time.sleep(2)
                oled.fill(0)

        if ir_sensor.value() == 1 and not registration_mode:
            uid = read_rfid()
            if uid and uid in authorized_rfid_uids:
                display_message(f"UID {uid} OK")
                control_solenoid(False)  # Desbloquear
            elif uid:
                display_message(f"UID {uid} NO")
                control_solenoid(True)  # Bloquear
            time.sleep(2)
            oled.fill(0)
        time.sleep(0.5)

def generate_unique_code():
    unique_code = str(random.randint(100000, 999999))
    unique_codes[unique_code] = time.time() + 300
    return unique_code

def generate_token():
    token = hashlib.sha256(str(time.time()).encode()).hexdigest()
    valid_tokens[token] = time.time() + 300
    return token

def check_user_credentials(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return username in authorized_users and authorized_users[username] == hashed_password

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

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

@app.route('/start_registration', methods=['GET'])
def start_registration():
    global registration_mode
    registration_mode = True
    return jsonify({"message": "Modo de registro activado"})

@app.route('/stop_registration', methods=['GET'])
def stop_registration():
    global registration_mode
    registration_mode = False
    return jsonify({"message": "Modo de registro desactivado"})

@app.route('/register_uid/<uid>', methods=['POST'])
def register_uid(uid):
    if registration_mode:
        authorized_rfid_uids.add(uid)
        return jsonify({"message": f"UID {uid} registrado exitosamente"})
    else:
        return jsonify({"error": "Modo de registro no activado"}), 403

if __name__ == '__main__':
    threading.Thread(target=access_control_loop).start()
    app.run(host='0.0.0.0', port=80)
