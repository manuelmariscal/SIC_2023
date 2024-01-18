import hashlib
import time
from SIC_2023.pyhtonScripts.RFID_OOP import ULTRASONIC_ECHO_PIN, ULTRASONIC_TRIGGER_PIN
from flask import Flask, request, jsonify
from gpiozero import DistanceSensor


class RFIDReaderWriter:
    def __init__(self):
        self.reader = SimpleMFRC522()

    def read_card(self):
        id, text = self.reader.read()
        return id, text

    def write_card(self, text):
        self.reader.write(text)
        print("Escrito correctamente")

    def clean_up(self):
        GPIO.cleanup()

class DistanceSensorHandler:
    def __init__(self, trigger_pin, echo_pin):
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)

    def is_object_close(self, threshold=15):
        distance = self.sensor.distance * 100  # Convertir a cm
        return distance < threshold

class LEDHandler:
    def __init__(self, red_pin, yellow_pin, green_pin):
        self.led_red = LED(red_pin)
        self.led_yellow = LED(yellow_pin)
        self.led_green = LED(green_pin)

    def red_on(self):
        self.led_red.on()

    def red_off(self):
        self.led_red.off()

    def yellow_on(self):
        self.led_yellow.on()

    def yellow_off(self):
        self.led_yellow.off()

    def green_blink(self, blink_time=5):
        self.led_green.blink(on_time=1, off_time=1, n=blink_time, background=False)

class RFIDSystem:
    
    def __init__(self):
        
        self.rfid = RFIDReaderWriter()
        self.ultrasonic = DistanceSensorHandler(ULTRASONIC_TRIGGER_PIN, ULTRASONIC_ECHO_PIN)
        self.leds = LEDHandler(LED_RED_PIN, LED_YELLOW_PIN, LED_GREEN_PIN)
        self.app = Flask(__name__)

        @self.app.route('/get_one_time_code', methods=['GET'])
        def get_one_time_code():
            # En esta función, puedes manejar la solicitud GET de la aplicación
            # Aquí puedes generar y devolver el token de un solo uso

            one_time_code = self.generate_one_time_code()

            return jsonify({'one_time_code': one_time_code})

    def generate_one_time_code(self):
        
        # Genera un código de un solo uso basado en el tiempo actual
        current_time = str(int(time.time()))  # Obtén el tiempo actual en segundos
        secret_key = "SECRET_KEY_HERE"  # Reemplaza con tu clave secreta
        code = hashlib.sha256((current_time + secret_key).encode()).hexdigest()
        return code

    def handle_rfid_access(self):
        try:
            while True:
                if self.ultrasonic.is_object_close():
                    self.leds.yellow_on()
                    mode = input("Ingrese 'E' para modo escritura o 'L' para modo lectura: ").upper()
                    if mode == "E":
                        text_to_write = input("Ingrese el texto para escribir en la tarjeta: ")
                        self.rfid.write_card(text_to_write)
                    elif mode == "L":
                        id, text = self.rfid.read_card()
                        print(f"ID: {id}, Texto: {text}")
                    else:
                        print("Modo no válido")
                    self.leds.yellow_off()
                else:
                    self.leds.red_on()
                    time.sleep(1)
                    self.leds.red_off()
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Programa terminado por el usuario")
        finally:
            self.rfid.clean_up()

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    rfid_system = RFIDSystem()
    rfid_system.run()
