#Verifica las funciones de la CPU

import psutil

print(psutil.cpu_percent(interval = 1)) #Comprueba el %  de uso de CPU
print(psutil.cpu_count()) #Comprueba el numero de CPU fisicas