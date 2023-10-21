import RPi.GPIO as GPIO
import psutil
import time

# Configura los pines GPIO para los indicadores LED
LED_GREEN_PIN = 17
LED_RED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_GREEN_PIN, GPIO.OUT)
GPIO.setup(LED_RED_PIN, GPIO.OUT)

# Umbral de uso de la CPU para encender el indicador rojo
UMBRAL_ROJO = 80

def main():
    try:
        while True:
            # Obtén el porcentaje de uso de la CPU
            cpu_percent = psutil.cpu_percent(interval=1)

            # Enciende el indicador verde si el uso de la CPU es bajo, de lo contrario, enciende el indicador rojo
            if cpu_percent < UMBRAL_ROJO:
                GPIO.output(LED_GREEN_PIN, GPIO.HIGH)
                GPIO.output(LED_RED_PIN, GPIO.LOW)
            else:
                GPIO.output(LED_GREEN_PIN, GPIO.LOW)
                GPIO.output(LED_RED_PIN, GPIO.HIGH)

    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
