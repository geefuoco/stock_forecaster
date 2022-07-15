from flask import Flask, Response, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return {"text": "Hello"}


@app.route("/predict/AAPL", methods=["GET", "OPTIONS"])
def prediction():
    print("hit")
    resp = jsonify({"price": 148.90})
    resp.headers["Access-Control-Allow-Origin"] = "http://192.168.2.210:3000"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp
