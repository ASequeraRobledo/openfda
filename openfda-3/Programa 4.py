# Importamos los módulos y bibliotecas necesarios para realizar este programa
import socketserver
import http.server
import http.client
import json
IP = "127.0.0.1"
PORT = 9000
MAX_OPEN_REQUESTS = 5 # Puede recibir un máximo de 5 solicitudes

# Empleamos un código que utiliza la biblioteca http.client que hemos importado para leer repositorios
# Gracias a este código podremos obtener
headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=11", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
informacion = json.loads(repos_raw)
medicamento_info = informacion["results"]
lista = []
for i in medicamento_info:# Iteramos sobre las variables que tiene la página
    if i['openfda']:
        nombre = i['openfda']['brand_name'][0]
        lista.append(nombre)
    else:
        nombre = "Medicamento no disponible" # Condición que evalúa el caso en el que no aparezca un medicamento
        lista.append(nombre)

# sabemos que en la página a la que accedemos el contenido es json y json se encuentra en forma de diccionario por tanto utilizamos las funciones de un diccionario para encontrar los diferentes elementos

# Clase que se obtiene mediante herencia a partir de la clase BaseHTTPRequestHandler y en concreto por encapsulación
# La encapsulación consiste en que la clase que hemos creado puede cambiar el comportamiento de la clase de la que hereda de manera selectiva
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # Siempre se utiliza la función Get para invocar peticiones
    def do_GET(self):

        #  Envio de la respuesta al cliente
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

# Introducimos el contenido html que queremos que el servidor envíe al cliente
# Será el contenido que aparecerá en la página y que podra visualizar el cliente del servidor
        mensaje = """<html>
        <head>
        <meta charset = "utf-8">
        <title>Medicamentos</title>
        </head>
        <body style="background-color:lightblue">
        <h1>Medicamentos</h1>
        <p>Aquí podrá encontrar los nombres de diez medicamentos obtenidos de OpenFda:</p>
        <p>{}</p>
        <a href="https://api.fda.gov/drug/label.json?limit=10">Enlace a descripción de los medicamentos</a>
        <img src="http://www.openbiomedical.org/wordpress/wp-content/uploads/2015/09/openfda_logo.jpg?x10565.png"width=30% height=20%>
        </body>
        </html>""".format(lista)
        self.wfile.write(bytes(mensaje, "utf8"))
        print("Petición atendida!")

        return

# A partir de aquí comienzan las instrucciones del servidor
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("Sirviendo en puerto: {}".format(PORT))

try:

    httpd.serve_forever() # Se crea el servidor para "siempre"

# Tratamos el error en el caso de que el servidor deje de funcionar
except KeyboardInterrupt:

    print("Servidor detenido")

    httpd.server_close()