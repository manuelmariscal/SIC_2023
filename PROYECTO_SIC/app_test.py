from flask import Flask, render_template, request

app = Flask(__name__)

# Variables para el estado de los LEDs y el relé
led_red_state = False
led_green_state = False
relay_state = False

@app.route("/")
def index():
    return render_template(r"C:\Users\maris\SIC2023\SIC_2023\PROYECTO_SIC\index.html", red_led_state=led_red_state, green_led_state=led_green_state, relay_state=relay_state)

@app.route("/control", methods=["POST"])
def control():
    global led_red_state, led_green_state, relay_state

    user_input = request.form["user_input"].upper()

    if user_input == 'O':
        led_green_state = True
        led_red_state = False
        relay_state = True
    elif user_input == 'C':
        led_green_state = False
        led_red_state = True
        relay_state = False
    elif user_input == 'Q':
        return "Saliendo del programa."
    else:
        return "Entrada no válida. Ingresa 'O', 'C' o 'Q'."

    return render_template(r"C:\Users\maris\SIC2023\SIC_2023\PROYECTO_SIC\control.html", red_led_state=led_red_state, green_led_state=led_green_state, relay_state=relay_state)

if __name__ == "__main__":
    app.run(debug=True)
