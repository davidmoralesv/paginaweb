import time

import requests
from flask import Flask, render_template, request
from ubidots import ApiClient

app = Flask(__name__)
token = ""
api = None
diccionario_valores = {}
instancias_ubidots = []
nombre_dispositivos = []
metodo_puerta1, metodo_foco_cuarto1, metodo_foco_sala, metodo_foco_cocina = None, None, None, None
metodo_foco_cuarto2, metodo_foco_baño1, metodo_monitor1, metodo_ventilador = None, None, None, None
metodo_humedad, metodo_polucion, metodo_temperatura = None, None, None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/r")
def reload():
    obtener_instancias()
    get_values()
    return render_template("index.html")


@app.route("/Puertas", methods=['GET', 'POST'])
def puerta():
    valor_puerta1 = diccionario_valores.get('puerta1')
    valor_monitor1 = diccionario_valores.get('monitor1')
    valor_ventilador = diccionario_valores.get('ventilador')

    if request.method == 'POST':
        setear_valores()
        valor_puerta1 = diccionario_valores.get('puerta1')
        valor_monitor1 = diccionario_valores.get('monitor1')
        valor_ventilador = diccionario_valores.get('ventilador')

    valores_puertas_dispositivos = {
        "valor_puerta1": valor_puerta1,
        "valor_monitor1": valor_monitor1,
        "valor_ventilador": valor_ventilador
    }

    return render_template("controlPuerta.html", valores_puertas_dispositivos=valores_puertas_dispositivos)


@app.route("/Cuartos", methods=['GET', 'POST'])
def cuartos():
    valor_cuarto1 = diccionario_valores.get('foco_cuarto1')
    valor_cuarto2 = diccionario_valores.get('foco_cuarto2')

    if request.method == 'POST':
        setear_valores()
        valor_cuarto1 = diccionario_valores.get('foco_cuarto1')
        valor_cuarto2 = diccionario_valores.get('foco_cuarto2')

    valores_cuartos = {
        "valor_cuarto1": valor_cuarto1,
        "valor_cuarto2": valor_cuarto2
    }

    return render_template("controlCuartos.html", valores_cuartos=valores_cuartos)


@app.route("/Baños", methods=['GET', 'POST'])
def baños():
    valor_baño1 = diccionario_valores.get('foco_baño1')

    if request.method == 'POST':
        setear_valores()
        valor_baño1 = diccionario_valores.get('foco_baño1')

    valores_baños = {
        "valor_baño1": valor_baño1
    }

    return render_template("controlBaños.html", valores_baños=valores_baños)


@app.route("/SalaYCocina", methods=['GET', 'POST'])
def salaCocina():
    valor_sala = diccionario_valores.get('foco_sala')
    valor_cocina = diccionario_valores.get('foco_cocina')

    if request.method == 'POST':
        setear_valores()
        valor_sala = diccionario_valores.get('foco_sala')
        valor_cocina = diccionario_valores.get('foco_cocina')

    valores_SalaCocina = {
        "valor_sala": valor_sala,
        "valor_cocina": valor_cocina
    }

    return render_template("controlSalaCocina.html", valores_SalaCocina=valores_SalaCocina)


@app.route("/Estadisticas", methods=['GET', 'POST'])
def estadisticas():
    valor_humedad = metodo_humedad.get_values(1)[0].get("value")
    valor_temperatura = metodo_temperatura.get_values(1)[0].get("value")
    valor_polucion = metodo_polucion.get_values(1)[0].get("value")

    height = ((valor_temperatura + 20) / 70) * 100
    data_value = valor_temperatura

    valores = {"valor_humedad": valor_humedad, "height": height, "data_value": data_value,
               "valor_polucion": valor_polucion}

    if request.method == "POST":
        return valores

    if request.method == "GET":
        return render_template("controlEstadisticas.html", valores_estadisticas=valores)


@app.route("/About")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("Error.html")


def crear_token():
    status = 400
    attempts = 0

    url = 'https://industrial.api.ubidots.com/api/v1.6/auth/token'
    headers = {"x-ubidots-apikey": "BBFF-f982452f59fb11f99b8ab4ef539b2f1413f", "Content-Type": "application/json"}

    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers)
        status = req.status_code
        attempts += 1
        if status >= 400:
            time.sleep(1)

    if status >= 400:
        print("Error, no puedo enviar los datos después de 5 intentos")
        return False

    return req.json().get("token")


def get_values():
    diccionario_valores["puerta1"] = metodo_puerta1.get_values(1)[0].get("value")
    diccionario_valores["foco_cuarto1"] = metodo_foco_cuarto1.get_values(1)[0].get("value")
    diccionario_valores["foco_sala"] = metodo_foco_sala.get_values(1)[0].get("value")
    diccionario_valores["foco_cocina"] = metodo_foco_cocina.get_values(1)[0].get("value")
    diccionario_valores["foco_cuarto2"] = metodo_foco_cuarto2.get_values(1)[0].get("value")
    diccionario_valores["foco_baño1"] = metodo_foco_baño1.get_values(1)[0].get("value")
    diccionario_valores["monitor1"] = metodo_monitor1.get_values(1)[0].get("value")
    diccionario_valores["ventilador"] = metodo_ventilador.get_values(1)[0].get("value")

    return diccionario_valores


def get_ids():
    diccionario_ids = {
        "id_puerta1": "5ceb3ce41d84724e6678ba07",
        "id_foco_cuarto1": "5ceb3d3e1d84724e50e3cab2",
        "id_foco_sala": "5ceb3c9e1d84724ea4df3a5f",
        "id_foco_cocina": "5ceb3c961d84724b7e9536c2",
        "id_foco_cuarto2": "5ceb3d331d84724e50e3caac",
        "id_foco_baño1": "5ceb3cbf1d84724f01cccfe8",
        "id_monitor1": "5ceb43381d847252582bf1a3",
        "id_ventilador": "5ceb3cd61d84724f32e0d38b",
        "id_humedad": "5ceb3dd41d84724f01cccff9",
        "id_temperatura": "5ceb3dcf1d8472502f76df2b",
        "id_polucion": "5ceb3de91d84724a855230fc"
    }
    return diccionario_ids


def obtener_instancias():
    global token, api, metodo_puerta1, metodo_foco_cuarto1, metodo_foco_sala, metodo_foco_cocina
    global metodo_foco_cuarto2, metodo_foco_baño1, metodo_monitor1, metodo_ventilador, metodo_temperatura, metodo_humedad, metodo_polucion
    global diccionario_valores
    global instancias_ubidots, nombre_dispositivos

    if token == "":
        token = crear_token()
    api = ApiClient(token=token, base_url="http://industrial.api.ubidots.com/api/v1.6/")

    metodo_puerta1 = api.get_variable(get_ids().get("id_puerta1"))
    instancias_ubidots.append(metodo_puerta1)
    nombre_dispositivos.append("puerta1")

    metodo_foco_cuarto1 = api.get_variable(get_ids().get("id_foco_cuarto1"))
    instancias_ubidots.append(metodo_foco_cuarto1)
    nombre_dispositivos.append("foco_cuarto1")

    metodo_foco_sala = api.get_variable(get_ids().get("id_foco_sala"))
    instancias_ubidots.append(metodo_foco_sala)
    nombre_dispositivos.append("foco_sala")

    metodo_foco_cocina = api.get_variable(get_ids().get("id_foco_cocina"))
    instancias_ubidots.append(metodo_foco_cocina)
    nombre_dispositivos.append("foco_cocina")

    metodo_foco_cuarto2 = api.get_variable(get_ids().get("id_foco_cuarto2"))
    instancias_ubidots.append(metodo_foco_cuarto2)
    nombre_dispositivos.append("foco_cuarto2")

    metodo_foco_baño1 = api.get_variable(get_ids().get("id_foco_baño1"))
    instancias_ubidots.append(metodo_foco_baño1)
    nombre_dispositivos.append("foco_baño1")

    metodo_monitor1 = api.get_variable(get_ids().get("id_monitor1"))
    instancias_ubidots.append(metodo_monitor1)
    nombre_dispositivos.append("monitor1")

    metodo_ventilador = api.get_variable(get_ids().get("id_ventilador"))
    instancias_ubidots.append(metodo_ventilador)
    nombre_dispositivos.append("ventilador")

    metodo_humedad = api.get_variable(get_ids().get("id_humedad"))
    metodo_temperatura = api.get_variable(get_ids().get("id_temperatura"))
    metodo_polucion = api.get_variable(get_ids().get("id_polucion"))


def setear_valores():
    nombre = request.form.to_dict().get("nombre")
    estado = request.form.to_dict().get("estado")

    for instancia, nom_dispositivo in zip(instancias_ubidots, nombre_dispositivos):
        if nombre == nom_dispositivo:
            valor = 1.0 if (estado == 'true') else 0.0
            instancia.save_value({'value': valor})
            diccionario_valores[nom_dispositivo] = valor
