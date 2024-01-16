from flask import Flask, render_template, request
from machine import Pin
import time

app = Flask(__name__)

# Define los pines GPIO
LED_RED = Pin(4, Pin.OUT)
LED_GREEN = Pin(5, Pin.OUT)
RELAY = Pin(3, Pin.OUT)
BUZZER = Pin(2, Pin.OUT)

def activate_relay():
    RELAY.on()

def deactivate_relay():
    RELAY.off()

# Función para encender el LED rojo y apagar el verde
def turn_on_red_led():
    LED_RED.on()
    LED_GREEN.off()

# Función para encender el LED verde y apagar el rojo
def turn_on_green_led():
    LED_RED.off()
    LED_GREEN.on()

# Función para activar el zumbador
def activate_buzzer():
    BUZZER.on()
    time.sleep(0.5)
    BUZZER.off()

@app.route("/")
def index():
    red_led_status = "Encendido" if LED_RED.value() else "Apagado"
    green_led_status = "Encendido" if LED_GREEN.value() else "Apagado"
    relay_status = "Encendido" if RELAY.value() else "Apagado"
    return render_template("index.html", red_led_status=red_led_status, green_led_status=green_led_status, relay_status=relay_status)

@app.route("/control", methods=["POST"])
def control():
    user_input = request.form["user_input"].upper()

    if user_input == 'O':
        turn_on_green_led()
        activate_buzzer()
        activate_relay()
        message = "LED Verde encendido."
    elif user_input == 'C':
        turn_on_red_led()
        activate_buzzer()
        deactivate_relay()
        message = "LED Rojo encendido."
    elif user_input == 'Q':
        message = "Saliendo del programa."
    else:
        message = "Entrada no válida. Ingresa 'O', 'C' o 'Q'."

    return render_template("control.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
