from gpiozero import LED

led_red = LED(20)
#LED permanece encendido infinitamente
while True:
    led_red.on()