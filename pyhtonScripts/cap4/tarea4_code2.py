from gpiozero import MCP3000, DistanceSensor, Button, LED
from datetime import datetime
from time import sleep

pot = MCP3000(7)
ultrasonic = DistanceSensor(echo=21, trigger=20)
button = Button(2)  # Cambia 2 al número de pin correcto para tu botón
led = LED(17)  # Cambia 17 al número de pin correcto para tu LED

file = open('/home/pi/Unit_Practice/distance_log.txt', 'w')

def main():
    while True:
        button.wait_for_press()  # Espera hasta que se presione el botón
        
        dist = ultrasonic.distance * 100
        span = pot.value * 100
        
        dist, span = round(dist, 3), round(span, 3)
        
        if dist <= span:
            print(f"scaled span: {span}, dist: {dist}")
            timestamp = datetime.now().strftime('%Y/%m/%d - %H:%M:%S')
            data = f"{timestamp} --> " \
                    f"distance: {dist}, span: {span}\n"
            file.write(data)
            file.flush()  # Asegura que los datos se escriban en el archivo
            led.on()
        else:
            print(f"Distance > span!! scaled span: {span}, dist: {dist}")
            
        sleep(1)
        led.off()  # Apaga el LED después de la medición

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        file.close()
