from flask import Flask, Response, jsonify
from lib import model_handler

app = Flask(__name__)

host = "http://192.168.2.210"
port = 3000


@app.route("/")
def index():
    return {"text": "Hello"}


@app.route("/predict/<ticker>", methods=["get", "options"])
def prediction(ticker: str):
    prediction = model_handler.get_prediction_for(ticker)
    resp = jsonify({"price": prediction})
    resp.headers["Access-Control-Allow-Origin"] = f"{host}:{port}"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp
