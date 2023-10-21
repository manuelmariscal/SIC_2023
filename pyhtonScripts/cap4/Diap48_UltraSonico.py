import RPi.GPIO as GPIO
import time

# Configura los pines del sensor ultrasónico
TRIG_PIN = 23  # Pin del trigger
ECHO_PIN = 24  # Pin del eco

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    # Genera un pulso en el pin TRIG para activar la medición
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    pulse_start = 0
    pulse_end = 0

    # Espera hasta que el pin ECHO se ACTIVE (HIGH)
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()

    # Espera hasta que el pin ECHO se DESACTIVE (LOW)
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    # Calcula la distancia en centímetros
    distance = (pulse_duration * 34300) / 2

    return distance

try:
    while True:
        distance = measure_distance()
        print(f"Distancia: {distance:.2f} cm")
        time.sleep(1)  # Puedes ajustar la frecuencia de lectura según tus necesidades

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
