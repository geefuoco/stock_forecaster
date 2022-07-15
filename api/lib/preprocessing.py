import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def train_test_split(X, y, train_size=0.8):
    assert len(X) == len(y)
    size = int(len(X) * train_size)
    X_train, X_test = X[:size, :], X[size:, :]
    y_train, y_test = y[:size], y[size:]
    return X_train, y_train, X_test, y_test


class Preprocessor:
    def __init__(self):
        self._x_scaler = MinMaxScaler()
        self._y_scaler = MinMaxScaler()

    def preprocess(self, X, target_column="Close", time_lag=2):
        """
        Fully preprocess data by applying adding 50 exponential moving average,
        25 simple moving average, and a timelag. Returns the data scaled

        X: pd.DataFrame\t Data to preprocess
        target_column: str\t Column that will be used as the target variable
        time_lag: int\t The time lag to add to each obersvation
        returns: np.array\t Scaled x, y
        """
        data = self.create_50_ema(X, [target_column])
        data = self.create_25_ma(X, [target_column])
        data = self.timelag_data(X, time_lag).dropna()
        target = data[[target_column]]
        data = data.drop(target_column, axis=1)
        x_scaled, y_scaled = self.scale(data, target)
        return x_scaled, y_scaled

    def reshape(self, X):
        """
        Reshape data into format for LSTM
        X: np.array
        """
        return X.reshape(X.shape[0], X.shape[1], 1)

    def scale(self, X, y=None):
        """
        Scales data with a min max scaler and returns it

        X: array-like\tData to scale
        y: array-like\ttarget value to scale (using separate scaler)
        """
        y_scaled = None
        if y is not None:
            y_scaled = self._y_scaler.fit_transform(y)
        X_scaled = self._x_scaler.fit_transform(X)
        return X_scaled, y_scaled

    def unscale_target(self, y):
        """
        Unscales data

        y: np.array
        returns: np.array
        """
        return self._y_scaler.inverse_transform(y)

    def create_50_ema(self, X: pd.DataFrame, columns: list[str]):
        """
        Creates a feature for the 50 exponential moving average for given column

        X: pd.DataFrame\t Dataframe to add the colums to
        columns: list[str]\t List of columns to target
        """
        data = X.copy()
        for col in columns:
            data[f"{col}_50_ema"] = data[col].ewm(span=50, adjust=False).mean()
        return data

    def create_25_ma(self, X: pd.DataFrame, columns: list[str]):
        """
        Creates a feature for the 25 moving average for given column

        X: pd.DataFrame\t Dataframe to add the colums to
        columns: list[str]\t List of columns to target
        """
        data = X.copy()
        for col in columns:
            data[f"{col}_25_ma"] = data[col].rolling(window=25).mean()
        return data.dropna()

    def timelag_data(self, X: pd.DataFrame, timelag: int):
        """
        Creates new featues for representing the prior days for specified columns

        X: pd.DataFrame\tDataframe to udpate
        timelag: int\t The timelag to add to each column
        """
        data = self._remove_features(X, ["Date", "Adj Close"])
        t = []
        for i in range(timelag):
            t.append(data.shift(i + 1))
        for i in range(len(t)):
            df = t[i]
            df.columns = [f"t-{i+1}_{col}" for col in df.columns]
        data = pd.concat((data, *t), axis=1)
        data = self._remove_features(data, ["High", "Open", "Low", "Volume"])
        return data

    def _remove_features(self, X: pd.DataFrame, columns: list[str]):
        """
        Removes features from the DataFrame and returns it
        X: pd.DataFrame\t DataFrame to remove features from
        """
        return X.drop(columns=columns)
