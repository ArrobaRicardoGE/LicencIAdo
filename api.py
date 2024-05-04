from flask import Flask, request
from model.model import Model

app = Flask(__name__)
m = Model()


"""
Spec:
POST /pregunta
{
    "pregunta": str
}

Returns JSON
{
    "respuesta": str
    "contexto": [
        "ley": str,
        "numero": str,
        "titulo': str | null,
        "capitulo": str | null,
        "texto": str,
    ]
}
"""


@app.post("/pregunta")
def pregunta():
    pregunta = request.json.get("pregunta", None)
    if not pregunta:
        return {"error": "Pregunta invaida. Revisa el formato"}

    res, ctx = m.ask_question(pregunta)
    return {"respuesta": res, "contexto": ctx}
