from tensorflow.keras.models import load_model
from .preprocessing import Preprocessor
from .data_gathering import fetch_new_observation
from datetime import datetime, time, timezone, timedelta
import os
import traceback


_data_path = os.path.join(os.path.dirname(__file__), "./data/")
next_update = None


def get_prediction_for(ticker: str):
    """
    Get today's price prediction for the specified ticker
    """
    file = f"{_data_path + ticker}.txt"
    if os.path.exists(file):
        last_file_save = datetime.fromtimestamp(os.path.getmtime(file)).date()
        today = datetime.today().date()
        if last_file_save == today:
            value = get_prediction_from_file(ticker)
            return value
    else:
        try:
            update_model(ticker)
            path = os.path.join(os.path.dirname(__file__), f"./models/{ticker}_model")
            if not os.path.exists(path):
                return f"Model not trained on {ticker}"
            model = load_trained_model(ticker)
            if model is None:
                return
            new_data = fetch_new_observation(ticker)
            x, _, proc = preprocess(new_data)
            x = x[-1].reshape(1, x.shape[1], x.shape[2])
            pred = model.predict(x)
            unscaled = proc.unscale_target(pred).flatten()
            value = unscaled[-1]
            save_prediction_to_file(ticker, str(value))
            return value
        except Exception:
            print(f"Could not find model for company {ticker}")
            print(traceback.format_exc())


def get_prediction_from_file(ticker: str):
    """
    Read the prediction from a file
    """
    if os.path.exists(f"{_data_path + ticker}.txt"):
        with open(f"{_data_path + ticker}.txt", "r") as f:
            value = f.readline()
        print("Reading value: ", value)
        return value


def save_prediction_to_file(ticker: str, value: str):
    """Save the prediction value to file"""
    print("Saving value: ", value)
    with open(f"{_data_path +ticker}.txt", "w") as f:
        f.write(value)


def update_model(ticker):
    """
    Update the model on newest data if it is available
    """
    global next_update
    if not after_market_close():
        print("Not after market close")
        return
    now = datetime.today().astimezone(tz=timezone.utc)
    if next_update is not None and not now >= next_update:
        print("Not time to update yet")
        return
    next_update = datetime.today().astimezone(tz=timezone.utc) + timedelta(1)
    print("updating model")
    new_data = fetch_new_observation(ticker)
    if new_data is not None:
        model = load_trained_model(ticker)
        if model is not None:
            model, _ = train_on_new_data(model, new_data)
            save_model(model, ticker)


def after_market_close():
    today = datetime.today().astimezone(tz=timezone.utc).date()
    market_close = datetime(
        today.year, today.month, today.day, 20, 0, 0, tzinfo=timezone.utc
    )
    now = datetime.now().astimezone(tz=timezone.utc)
    return now > market_close and now.weekday() < 5


def train_on_new_data(model, new_data):
    """
    Trains the model on new data and returns the model back with loss history
    """
    x, y, _ = preprocess(new_data)
    x = x[-1].reshape(1, x.shape[1], x.shape[2])
    y = y[-1]
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
        path = os.path.join(os.path.dirname(__file__), f"./models/{ticker}_model")
        model = load_model(path)
        return model
    except Exception:
        print(f"An error occured while trying to load folder {ticker}_model in models")
        print(traceback.format_exc())


def save_model(model, ticker: str):
    """
    Saves a model to the models folder
    """
    try:
        model.save(f"./models/{ticker}_model")
    except Exception:
        print("An error occured while trying to save the model")
