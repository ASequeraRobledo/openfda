# Importamos los módulos y bibliotecas necesarios para realizar este programa
import http.client
import json
# Empleamos un código que utiliza la biblioteca http.client que hemos importado para leer repositorios
headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers) # Fase de petición
r1 = conn.getresponse() # A partir de aquí la fase de respuesta
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

informacion = json.loads(repos_raw)

# sabemos que en la página a la que accedemos el contenido es json y json se encuentra en forma de diccionario por tanto utilizamos las funciones de un diccionario para encontrar los diferentes elementos
medicamento_info=informacion["results"][0]

# Imprimimos los elementos que se nos dice en el enunciado accediendo a ellos mediante las propiedades de los diccionarios
print("Id del medicamento:",medicamento_info["id"])
print("El medicamento es usado para:",medicamento_info["purpose"][0])
print("El medicamento lo fabrica:",medicamento_info["openfda"]["manufacturer_name"])
