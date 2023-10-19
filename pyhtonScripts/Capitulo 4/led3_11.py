from gpiozero import LED

led_red  = LED(20)

#Comprueba la salida y el LED mientras enciende, se apaga u otra cadena de entrada
while True:
    s = input()
    if s == "on":
        led_red.on()
    elif s == "off":
        led_red.off()
    else:
        print("invalid command")