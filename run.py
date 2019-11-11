import time

import requests
from flask import Flask, render_template, request, url_for
from ubidots import ApiClient
from werkzeug.utils import redirect

app = Flask(__name__)

token = ""
api = None
diccionario_valores = {}
instancias_ubidots = []
nombre_dispositivos = []


@app.route("/")
def index():
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
    try:

        valor_humedad = instancias_ubidots[5].get_values(1)[0].get("value")
        valor_temperatura = instancias_ubidots[9].get_values(1)[0].get("value")
        valor_polucion = instancias_ubidots[7].get_values(1)[0].get("value")

        height = ((valor_temperatura + 20) / 70) * 100
        data_value = valor_temperatura

        valores = {"valor_humedad": valor_humedad, "height": height, "data_value": data_value,
                   "valor_polucion": valor_polucion}
    except Exception as e:
        error = "Hubo un error obteniendo los valores del API de ubidots"
        return redirect(url_for("error", error=error))

    if request.method == "POST":
        return valores

    if request.method == "GET":
        return render_template("controlEstadisticas.html", valores_estadisticas=valores)


@app.route("/About")
def about():
    return render_template("about.html")


@app.errorhandler(Exception)
@app.route("/Error")
def error(e):
    error = request.args.get('error')
    return render_template("error.html", error=error)


def crear_token():
    status = 400
    attempts = 0

    url = 'https://industrial.api.ubidots.com/api/v1.6/auth/token'
    headers = {"x-ubidots-apikey": "BBFF-f982452f59fb11f99b8ab4ef539b2f1413f", "Content-Type": "application/json"}
    req = {}
    try:
        while status >= 400 and attempts <= 5:
            req = requests.post(url=url, headers=headers)
            status = req.status_code
            attempts += 1
            if status >= 400:
                time.sleep(1)

    except Exception as e:
        error = "Hubo un error intentando obtener el token"
        return redirect(url_for("error", error=error))
    if status >= 400:
        error = "Se excedió el número de intentos para obtener un token válido"
        return redirect(url_for("error", error=error))

    return req.json().get("token")


def get_values():
    diccionario_valores["foco_baño1"] = instancias_ubidots[0].get_values(1)[0].get("value")
    diccionario_valores["foco_cocina"] = instancias_ubidots[1].get_values(1)[0].get("value")
    diccionario_valores["foco_cuarto1"] = instancias_ubidots[2].get_values(1)[0].get("value")
    diccionario_valores["foco_cuarto2"] = instancias_ubidots[3].get_values(1)[0].get("value")
    diccionario_valores["foco_sala"] = instancias_ubidots[4].get_values(1)[0].get("value")
    diccionario_valores["monitor1"] = instancias_ubidots[6].get_values(1)[0].get("value")
    diccionario_valores["puerta1"] = instancias_ubidots[8].get_values(1)[0].get("value")
    diccionario_valores["ventilador"] = instancias_ubidots[10].get_values(1)[0].get("value")

    return diccionario_valores


def get_ids():
    diccionario_ids = {
        "id_foco_baño1": "5ceb3cbf1d84724f01cccfe8",
        "id_foco_cocina": "5ceb3c961d84724b7e9536c2",
        "id_foco_cuarto1": "5ceb3d3e1d84724e50e3cab2",
        "id_foco_cuarto2": "5ceb3d331d84724e50e3caac",
        "id_foco_sala": "5ceb3c9e1d84724ea4df3a5f",
        "id_humedad": "5ceb3dd41d84724f01cccff9",
        "id_monitor1": "5ceb43381d847252582bf1a3",
        "id_polucion": "5ceb3de91d84724a855230fc",
        "id_puerta1": "5ceb3ce41d84724e6678ba07",
        "id_temperatura": "5ceb3dcf1d8472502f76df2b",
        "id_ventilador": "5ceb3cd61d84724f32e0d38b"
    }
    return diccionario_ids


def get_nombre_dispositivos():
    nombre_dis = ["foco_baño1", "foco_cocina", "foco_cuarto1", "foco_cuarto2", "foco_sala", "humedad",
                  "monitor1", "polucion", "puerta1", "temperatura", "ventilador"]
    return nombre_dis


def obtener_instancias():
    global token, api
    global diccionario_valores
    global instancias_ubidots, nombre_dispositivos

    if token == "":
        token = crear_token()
    if api is None:
        api = ApiClient(token=token, base_url="http://industrial.api.ubidots.com/api/v1.6/")

    try:
        lista_ids = [*get_ids().values()]
        nombre_dispositivos = get_nombre_dispositivos()
        if len(instancias_ubidots) > 0:
            return
        for id in lista_ids:
            instancias_ubidots.append(api.get_variable(id))

    except Exception as e:
        error = "Hubo un error obteniendo las instancias de ubidots."
        return redirect(url_for("error", error=error))


def setear_valores():
    nombre = request.form.to_dict().get("nombre")
    estado = request.form.to_dict().get("estado")

    try:
        for instancia, nom_dispositivo in zip(instancias_ubidots, nombre_dispositivos):
            if nombre == nom_dispositivo:
                valor = 1.0 if (estado == 'true') else 0.0
                instancia.save_value({'value': valor})
                diccionario_valores[nom_dispositivo] = valor
    except Exception as e:
        error = "Hubo un error guardando los valores en ubidots"
        return redirect(url_for("error", error=error))
