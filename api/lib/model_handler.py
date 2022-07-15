from tf.keras.models import load_model
from .preprocessing import Preprocessor
from .data_gathering import fetch_new_observation
from datetime import datetime, time, timezone
import os


def get_prediction_for(ticker: str):
    """
    Get today's price prediction for the specified ticker
    """
    try:
        update_model(ticker)
        path = f"./models/{ticker}_model"
        if not os.path.exists(path):
            return f"Model not trained on {ticker}"
        model = load_trained_model(ticker)
        new_data = fetch_new_observation(ticker)
        x, _, proc = preprocess(new_data)
        pred = model.predict(x)
        unscaled = proc.unscale_target(pred)
        return unscaled[-1]
    except Exception:
        print(f"Could not find model for company {ticker}")


def update_model(ticker):
    """
    Update the model on newest data if it is available
    """
    if not after_market_close():
        return
    new_data = fetch_new_observation(ticker)
    if new_data is not None:
        model = load_trained_model(ticker)
        if model is not None:
            model, _ = train_on_new_data(model, new_data)
            save_model(model, ticker)


def after_market_close():
    close = time(20, 0, 0)
    today = datetime.today().astimezone(tz=timezone.utc).date()
    market_close = datetime.combine(today, close)
    now = datetime.now().astimezone(tz=timezone.utc)
    return now > market_close


def train_on_new_data(model, new_data):
    """
    Trains the model on new data and returns the model back with loss history
    """
    x, y = preprocess(new_data)
    hist = model.fit(x, y)
    return model, hist.history["loss"]


def preprocess(new_data):
    processor = Preprocessor()
    x, y = processor.preprocess(new_data, "Close", 1)
    x = processor.reshape(x)
    return x, y, processor


def load_trained_model(ticker: str):
    """
    Loads in trained model for the given ticker
    """
    try:
        model = load_model(f"./models/{ticker}_model")
        return model
    except Exception:
        print(f"An error occured while trying to load folder {ticker}_model in models")


def save_model(model, ticker: str):
    """
    Saves a model to the models folder
    """
    try:
        model.save(f"./models/{ticker}_model")
    except Exception:
        print("An error occured while trying to save the model")
