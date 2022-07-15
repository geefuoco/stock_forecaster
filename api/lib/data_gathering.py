import pandas_datareader.data as reader
from datetime import date, timedelta


def fetch_new_observation(ticker: str):
    """
    Returns a stock dataframe with past two days
    ticker: str\t The stock symbol
    """

    today = date.today()
    start = today - timedelta(5)
    try:
        stock = reader.DataReader(ticker, start=start, end=today, data_source="yahoo")
        return stock.reset_index().tail(2)
    except Exception:
        print(f"An error has occured while trying to get data for {ticker}")
