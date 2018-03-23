
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

informacion = json.loads(repos_raw)

#sabemos que en api tenemos un diccionario, por tanto utilizamos las funciones de un diccionario para encontrar los diferentes elementos
medicamento_info=informacion["results"][0]

print("Id del medicamento",medicamento_info["id"])
print("El medicamento es usado para:",medicamento_info["purpose"][0])
print("El medicamento lo fabrica:",medicamento_info["openfda"]["manufacturer_name"])