# Importamos los módulos y bibliotecas necesarios para realizar este programa
import http.client
import json

# Empleamos un código que utiliza la biblioteca http.client que hemos importado para leer repositorios
headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers) # Con limit=10 encontraremos 10 medicamentos distintos
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
informacion = json.loads(repos_raw)

# sabemos que en la página a la que accedemos el contenido es json y json se encuentra en forma de diccionario por tanto utilizamos las funciones de un diccionario para encontrar los diferentes elementos
medicamento_info=informacion["results"]

# Indexamos entre los distintos elementos de la página para imprimir los diez que hay en ella
for i in range(len(medicamento_info)):
    info = medicamento_info[i]
    print("Id del medicamento:",info["id"])
