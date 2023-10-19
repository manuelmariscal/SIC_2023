#Comprueba las funciones relacionadas con el disco de psutil

import psutil

print(psutil.disk_partitions()) #Comprueba las particiones de disco montadas.

print(psutil.disk_usage('/')) #Muestra estadisticas del disco