#LED parpadenado en un ciclo especifico

from gpiozero import LED
from signal import pause

led_red = LED(20)

led_red.blink(1) #el led enciende un segundo y se apaga un segundo
pause()