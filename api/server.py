from flask import Flask, Response, jsonify
from flask_caching import Cache
from lib import model_handler

config = {"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300}

app = Flask(__name__, static_folder="../dist", static_url_path="/")

app.config.from_mapping(config)
cache = Cache(app)

host = "0.0.0.0"
port = 8000


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/predict/<ticker>", methods=["options"])
def options_prediction(ticker: str):
    resp = Response(status=200)
    resp.headers["Access-Control-Allow-Origin"] = f"{host}:{port}"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@app.route("/predict/<ticker>", methods=["get"])
@cache.cached()
def prediction(ticker: str):
    prediction = model_handler.get_prediction_for(ticker)
    prediction = "{:.2f}".format(float(prediction))
    resp = jsonify({"price": prediction})
    resp.headers["Access-Control-Allow-Origin"] = f"{host}:{port}"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp
