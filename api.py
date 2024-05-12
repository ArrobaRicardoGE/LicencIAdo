from flask import Flask, request, send_file
from flask_cors import CORS
from model.model import Model
import os
import urllib.parse as urlparse

app = Flask(__name__)
CORS(app)
m = Model()

HOST = os.environ.get("LICENCIADO_HOST")
LEY2FILE = {
    "Ley de Caminos Puentes y Autotransporte Federal": "LCPAF.pdf",
    "Ley de Movilidad y Transporte del Estado de Jalisco": "Ley de Movilidad y Transporte del Estado de Jalisco_2.pdf",
    "Ley General de Movilidad y Seguridad Vial": "LGMSV.pdf",
    "Reglamento de la Ley de Movilidad, Seguridad Vial y Transporte del Estado de Jalisco": "Reglamento de la Ley de Movilidad, Seguridad Vial y Transporte del Estado de Jalisco-230224.pdf",
    "Reglamento del Artículo Décimo Primero Transitorio de la Ley de los Servicios de Vialidad, Tránsito y Transporte del Estado de Jalisco": "Reglamento del Artículo Décimo Primero Transitorio de la Ley de los Servicios de Vialidad, Tránsito y Transporte del Estado de Jalisco.pdf",
    "Reglamento del Personal Operativo de la Secretaría de Vialidad": "Reglamento del Personal Operativo de la Secretaría de Vialidad.pdf",
    "Reglamento del Registro Estatal de  Movilidad y Transporte": "Reglamento del Registro Estatal de  Movilidad y Transporte.pdf",
    "Reglamento Interno del Organismo Coordinador de la Operación Integral del Servicio de Transporte Público": "Reglamento Interno del Organismo Coordinador de la Operación Integral del Servicio de Transporte Público.pdf",
    "Ley de Movilidad, Seguridad Vial y Transporte del Estado de Jalisco": "Ley de Movilidad, Seguridad Vial y Transporte del Estado de Jalisco-140823.pdf",
}

static_path = urlparse.urljoin(HOST, "/leyes/")
for ley, file in LEY2FILE.items():
    LEY2FILE[ley] = urlparse.urljoin(static_path, urlparse.quote(file))


def get_files(ctx):
    files = []
    seen = set()
    for v in ctx:
        ley = v["ley"]
        if ley not in LEY2FILE or ley in seen:
            continue
        seen.add(ley)
        files.append(
            {
                "url": LEY2FILE[ley],
                "name": ley,
            }
        )
    return files


"""
Spec:
POST /pregunta
{
    "pregunta": str
}

Returns JSON
{
    "respuesta": str,
    "contexto": [
        {
            "ley": str,
            "numero": str,
            "titulo': str | null,
            "capitulo": str | null,
            "texto": str
        }
    ],
    "files": [
        {
            "url": str,
            "name": str
        }
    ]
}
"""


@app.post("/pregunta")
def pregunta():
    pregunta = request.json.get("pregunta", None)
    if not pregunta:
        return {"error": "Pregunta inválida. Revisa el formato"}

    res, ctx = m.ask_question(pregunta)
    return {"respuesta": res, "contexto": ctx, "files": get_files(ctx)}


@app.get("/leyes/<name>")
def leyes(name):
    static_route = os.environ.get("LICENCIADO_STATIC_ROUTE")
    return send_file(os.path.join(static_route, name))
