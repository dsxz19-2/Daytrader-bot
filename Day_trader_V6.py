import yfinance as yf
from datetime import datetime, timedelta
import datetime as dt
import ta
import pandas as pd
import matplotlib.pyplot as plt


def get_data(ticker):
    end = datetime.now()
    start = end - timedelta(days=7)

    data_frame = yf.download(ticker, start=start, end=end, interval="1m")
    return data_frame


def obv_signal(data):
    # Calculate OBV
    data['PrevClose'] = data['Close'].shift(1)
    data['Direction'] = data['Close'] - data['PrevClose']
    data.loc[data['Direction'] > 0, 'OBV'] = data['Volume']
    data.loc[data['Direction'] < 0, 'OBV'] = -data['Volume']
    data['OBV'] = data['OBV'].cumsum()

    # Calculate EMA of OBV
    data['OBV_EMA'] = data['OBV'].ewm(span=20).mean()

    data['Signal'] = 'Hold'
    for i in range(1, len(data)):
        if data['OBV_EMA'][i - 1] < data['OBV_EMA'][i] < data['OBV'][i]:
            data.loc[data.index[i], 'Signal'] = 'Buy'

        elif data['OBV_EMA'][i - 1] > data['OBV_EMA'][i] > data['OBV'][i]:
            data.loc[data.index[i], 'Signal'] = 'Sell'

    return data.drop(['PrevClose', 'Direction'], axis=1)


data = obv_signal(get_data("SOL-CAD"))

budget = 1000000
starting = budget
amount = 10

# list(data["Signal"])[-i:][0]

for i in range(len(data)):
    if list(data["Signal"])[-i:][0] == "Buy":
        budget = budget - (list(data["Close"])[-i:][0])
        print(list(data["Close"])[-i:][0])

    if list(data["Signal"])[-i:][0] == "Sell":
        budget = budget + (list(data["Close"])[-i:][0])
        #print(budget - starting)


print(budget - starting)



