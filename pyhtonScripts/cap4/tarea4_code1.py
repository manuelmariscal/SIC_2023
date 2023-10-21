from gpiozero import LED
import psutil

# Definir los pines para los LEDs
led_rojo = LED(17)  # Cambia 17 al número de pin correcto para tu LED rojo
led_amarillo = LED(18)  # Cambia 18 al número de pin correcto para tu LED amarillo

# Obtener el uso del disco
uso_disco = psutil.disk_usage('/').percent

# Comprobar el uso del disco y tomar acciones
if uso_disco > 60:
    led_rojo.on()
elif uso_disco > 30:
    led_amarillo.on()

# Guardar el uso del disco en el archivo de registro
with open('/home/pi/Unit_Practice/disk_usage_log.txt', 'a') as archivo_log:
    archivo_log.write(f'Uso del disco: {uso_disco}%\n')
