import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from gpiozero import DistanceSensor, LED
import time

# Configuraciones de GPIO
RFID_PIN = 0  # Debes configurar esto según tus conexiones
ULTRASONIC_TRIGGER_PIN = 23
ULTRASONIC_ECHO_PIN = 24
LED_RED_PIN = 22
LED_YELLOW_PIN = 27
LED_GREEN_PIN = 17

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

    def run(self):
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

if __name__ == "__main__":
    rfid_system = RFIDSystem()
    rfid_system.run()
