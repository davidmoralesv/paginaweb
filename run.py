import time

import requests
from flask import Flask, render_template, request
from ubidots import ApiClient

app = Flask(__name__)
token = ""
api = None
diccionario_valores = {}
variable_foco_cuarto1, variable_foco_cuarto2, variable_foco_bano1, variable_foco_cocina = 0, 0, 0, 0


@app.route("/")
def index():
    obtener_instancias()
    get_values()
    return render_template("index.html")


@app.route("/templates/index.html")
def menu():
    return render_template("index.html")


@app.route("/templates/controlCuartos.html", methods=['GET', 'POST'])
def cuartos():
    valores_cuartos = {}
    valor_cuarto1 = diccionario_valores.get('foco_cuarto1')
    valor_cuarto2 = diccionario_valores.get('foco_cuarto2')

    if request.method == 'POST':
        breakpoint()
        if "cuarto1" in request.form:
            valor_cuarto1 = request.form.to_dict().get('cuarto1')
            variable_foco_cuarto1.save_value({'value': request.form.to_dict().get('cuarto1')})

        if "cuarto2" in request.form:
            variable_foco_cuarto2.save_value({'value': request.form.to_dict().get('cuarto2')})
            valor_cuarto2 = request.form.to_dict().get('cuarto2')

    # valores_cuartos = {
    #     "valor_cuarto1": diccionario_valores.get("foco_cuarto1"),
    #     "valor_cuarto2": diccionario_valores.get("foco_cuarto2")
    # }
    valores_cuartos = {
        "valor_cuarto1": valor_cuarto1,
        "valor_cuarto2": valor_cuarto2
    }

    breakpoint()

    return render_template("controlCuartos.html", valores_cuartos=valores_cuartos)


@app.route("/templates/controlBaños.html")
def baños():
    valores_banos = {
        "valor_bano1": diccionario_valores.get("foco_bano1")
    }
    return render_template("controlBaños.html", valores_banos=valores_banos)


@app.route("/templates/controlSalaCocina.html")
def salaCocina():
    return render_template("controlSalaCocina.html")


@app.route("/templates/controlPuerta.html")
def puerta():
    return render_template("controlPuerta.html")


@app.route("/templates/controlEstadisticas.html")
def estadisticas():
    return render_template("controlEstadisticas.html")


@app.route("/templates/about.html")
def about():
    return render_template("about.html")


def crear_token():
    status = 400
    attempts = 0

    url = 'https://industrial.api.ubidots.com/api/v1.6/auth/token'
    headers = {"x-ubidots-apikey": "BBFF-f982452f59fb11f99b8ab4ef539b2f1413f", "Content-Type": "application/json"}

    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    if status >= 400:
        print("Error, no puedo enviar los datos después de 5 intentos")
        return False

    return req.json().get("token")


def get_values():
    diccionario_valores["foco_cuarto1"] = variable_foco_cuarto1.get_values(1)[0].get("value")
    diccionario_valores["foco_cuarto2"] = variable_foco_cuarto2.get_values(1)[0].get("value")
    diccionario_valores["foco_bano1"] = variable_foco_bano1.get_values(1)[0].get("value")
    diccionario_valores["foco_cocina"] = variable_foco_cocina.get_values(1)[0].get("value")

    return diccionario_valores


def get_ids():
    diccionario_ids = {
        "id_foco_cuarto1": "5ceb3d3e1d84724e50e3cab2",
        "id_foco_cuarto2": "5ceb3d331d84724e50e3caac",
        "id_foco_bano1": "5ceb3cbf1d84724f01cccfe8",
        "id_foco_cocina": "5ceb3c961d84724b7e9536c2"
    }
    return diccionario_ids


def obtener_instancias():
    global token, api, variable_foco_cuarto1, variable_foco_cuarto2, variable_foco_bano1, variable_foco_cocina, \
        diccionario_valores

    token = crear_token()
    api = ApiClient(token=token, base_url="http://industrial.api.ubidots.com/api/v1.6/")

    variable_foco_cuarto1 = api.get_variable(get_ids().get("id_foco_cuarto1"))
    variable_foco_cuarto2 = api.get_variable(get_ids().get("id_foco_cuarto2"))
    variable_foco_bano1 = api.get_variable(get_ids().get("id_foco_bano1"))
    variable_foco_cocina = api.get_variable(get_ids().get("id_foco_cocina"))
