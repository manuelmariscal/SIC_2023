#Anexa el contenido existente de un archivo

f = open("test.txt", 'a') #Abre un archivo en modo anexar
for i in range(9,11):
    data = f"Added Line {i}!\n"
    f.write(data)
f.close()