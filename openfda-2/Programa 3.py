# Importamos los módulos y bibliotecas necesarios para realizar este programa
import http.client
import json

# Empleamos un código que utiliza la biblioteca http.client que hemos importado para leer repositorios
headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=20&search=active_ingredient:%22acetylsalicylic%22", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
informacion = json.loads(repos_raw)

#sabemos que en api tenemos un diccionario, por tanto utilizamos las funciones de un diccionario para encontrar los diferentes elementos
info=informacion["results"]

# Indexamos de la misma manera que en el programa 2 pero añadiendo que se imprima el nombre del fabricante
for a in range(len(info)):
    info_medicamento=info[a]
    print("Id del medicamento:", info_medicamento["id"])
    if info_medicamento["openfda"]:
        print("La aspirina es fabricada por:",info_medicamento["openfda"]["manufacturer_name"][0])
    else:
        print("Fabricante no disponible")