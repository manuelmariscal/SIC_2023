
from gpiozero import LED
from time import sleep

#Asignacion del numero de pin GPIO conectadi a cada LED como parametro
led ={
    "red" : LED(5),
    "yellow" : LED(6),
    "green" : LED(13)
}

#Metodo de parpadeo del LED secuencialmente
while True:
    for i in led.keys():
        led[1].blink(on_time=1, off_time=1)
        sleep(2)
