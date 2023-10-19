#Escribir archivo de texto

f = open("test.txt", 'w') #Se abre el archivo en modo escritura
for i in range(1,7): #Ciclo que escribe nuevo contenido
    data = f"Line {i}\n"
    f.write(data)
f.close()