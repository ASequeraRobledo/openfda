from flask import Flask
from flask import jsonify
from flask import request
import http.client
import json
import http.server

app = Flask(__name__)

#-------------------------------------------------------------------------------------------------------------------

#aquí tendríamos la parte en la que como clientes obtenemos información de la página openfda
#Creamos las listas que vamos a utilizar
headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=60", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
informacion = json.loads(repos_raw)
medicamento_info = informacion["results"]


#Documento del índice (tengo que introducir un input)
Index_html="""<html>
        <head>
        <meta charset = "utf-8">
        <title>Medicamentos</title>
        </head>
        <body style="background-color:lightblue">
        <h1>Indice</h1>
        <p>1-.)Información concreta sobre un medicamento</p>
        <a href="http://127.0.0.1:8000/formSearchDrug">Enlace a la página</a>
        <p>2-.)Información concreta sobre una empresa</p>
        <a href="http://127.0.0.1:8000/formSearchCompany">Enlace a la página</a>
        <p>3-.)Listado de medicamentos</p>
        <a href="http://127.0.0.1:8000/listDrugs">Enlace a la página</a>
        <p>4-.)Listado de empresas de medicamentos</p>
        <a href="http://127.0.0.1:8000/listCompanies">Enlace a la página</a>
        <img src="http://www.openbiomedical.org/wordpress/wp-content/uploads/2015/09/openfda_logo.jpg?x10565.png"width=30% height=20% align=right>
        <ul>Toda la información que pueden encontrar ha sido obtenida de las bases de Openfda</ul>
        </body>
        </html>"""


formulario_empresa="""<html>
        <head>
        <meta charset = "utf-8">
        <title>Medicamentos</title>
        </head>
        <body style="background-color:lightpink">
        <form action="/searchCompany" method="get">
        <div><label for="name">Company name:</label><input type="text" id="name" name="company_name" /></div><div class="button"><button type="submit">Send your message</button></div>
        </form>
        </html"""

formulario_drogas="""<html>
        <head>
        <meta charset = "utf-8">
        <title>Medicamentos</title>
        </head>
        <body style="background-color:lightblue">
        <form action="/searchDrug" method="get">
        <div><label for="name">Drug name:</label><input type="text" id="drug_name" name="name_ingredient" /></div><div class="button"><button type="submit">Send your message</button></div>
        </form>
        </html"""



#Creación de las listas
lista_medicamentos = []
lista_empresas=[]
for i in medicamento_info:# Iteramos sobre las variables que tiene la página
    if i['openfda']:
        nombre = i['openfda']['brand_name'][0]
        lista_medicamentos.append(nombre)
    else:
        nombre = "Medicamento no disponible" # Condición que evalúa el caso en el que no aparezca un medicamento
        lista_medicamentos.append(nombre)

for i in medicamento_info:# Iteramos sobre las variables que tiene la página
    if i['openfda']:
        nombre_2 = i['openfda']['manufacturer_name']
        lista_empresas.append(nombre_2)
    else:
        nombre_2 = "Empresa no disponible" # Condición que evalúa el caso en el que no aparezca un medicamento
        lista_empresas.append(nombre_2)

#---------------------------------------------------------------------------------

@app.route('/')
def getInicio():
    return Index_html

@app.route('/formSearchDrug',methods=['GET','POST'])
def getDrugAllEmpp():
    return formulario_drogas

@app.route('/searchDrug',methods=['GET','POST'])
def getAllEmpp():
    ingrediente = request.args.get('name_ingredient')
    #return ingrediente
    lista=["hola","adios"]
    return '''
    <html>
        <head>
            <title>Home Page - Microblog</title>
        </head>
        <body>
            <h1>Hello, ''' + lista[0]+ '''!</h1>
            <h1>Hello, ''' + ingrediente+ '''!</h1>
        </body>
    </html>'''

@app.route('/formSearchCompany', methods=['GET','POST']) #Me permite rellenar la url correctamente
def getpostAll():
    return formulario_empresa

@app.route('/searchCompany',methods=['GET','POST'])
def getAllEmp():
    company = request.args.get('company_name')
    return "Me has dicho"+company

@app.route('/listDrugs',methods=['GET'])
def getAllList() :
    return jsonify({'Drugs': lista_medicamentos})

@app.route('/listCompanies',methods=['GET'])
def getListCompanies():
    return jsonify({'Companies': lista_empresas})


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000)
