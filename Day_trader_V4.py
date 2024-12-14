# FAILED premium option not avaliable

import sys
import time
import ta
import requests
import json
import requests
import json
import pandas as pd
from re import T
from datetime import datetime


def buy(amount_of_coins):
    utc_now = datetime.utcnow()
    utc_now.strftime("%Y-%m-%d %I:%M")
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %I:%M")

    with open("orderV4.txt", "a") as f:
        f.write(f"\nBUY: {list(data_frame.Close)[-1:][0]} \n"
                f"Total Cost: {list(data_frame.Close)[-1:][0] * amount_of_coins} \n"
                f"UTC Time: {utc_now} \n"
                f"Local Time: {now} \n")
        f.close()


def sell(buy_price, sum_of_profits, amount_of_coins):
    utc_now = datetime.utcnow()
    utc_now = utc_now.strftime("%Y-%m-%d %I:%M")
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %I:%M")

    with open("orderV4.txt", "a") as f:
        f.write(f"\nSELL: {list(data_frame.Close)[-1:][0]} \n"
                f"Total Cost: {list(data_frame.Close)[-1:][0] * amount_of_coins} \n"
                f"Profit Of Trade: {list(data_frame.Close)[-1:][0] - buy_price} \n"
                f"Total Profits: {sum_of_profits} \n"
                f"UTC Time: {utc_now} \n"
                f"Local Time: {now} \n")
        f.close()


def main(amount_of_coins):
    key = "OHQCZSHPH96VE6IY"

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={sys.argv[1]}&market=CAD&interval=1min&apikey={key}'
    r = requests.get(url)

    data = json.loads(r.text)
    data = json.dumps(data["Time Series (1 min)"], indent=2)
    data = pd.read_json(data)
    data = data.T
    data["Open"] = data["1. open"]
    data["High"] = data["2. high"]
    data["Low"] = data["3. low"]
    data["Close"] = data["4. close"]
    data["Volume"] = data["5. volume"]
    data.drop("1. open", axis=1, inplace=True)
    data.drop("2. high", axis=1, inplace=True)
    data.drop("3. low", axis=1, inplace=True)
    data.drop("4. close", axis=1, inplace=True)
    data.drop("5. volume", axis=1, inplace=True)

    data["14-low"] = data["Low"].rolling(14).min()
    data["14-high"] = data["High"].rolling(14).max()
    data["RSI"] = ta.momentum.rsi(data.Close, window=14)
    k = data['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
    d = data['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
    data["MACD"] = k - d
    data["Signal"] = data["MACD"].ewm(span=9, adjust=False, min_periods=9).mean()
    data.dropna(inplace=True)

    rsi = list(data.RSI)[-1:][0]
    macd = list(data.MACD)[-1:][0]
    signal = list(data["Signal"])[-1:][0]
    print("[*********************100%***********************]  1 of 1 completed")
    print("RSI:", rsi)
    print("MACD:", macd)
    print("Signal:", signal)
    print("Close:", round(list(data.Close)[-1:][0], 2))
    print("Total Cost:", round(list(data.Close)[-1:][0], 2) * amount_of_coins)
    return rsi, macd, signal, data


trigger = 0
amount = 10
profits = []

while True:
    RSI, MACD, Signal, data_frame = main(amount)
    if (RSI > 53) and (MACD > Signal):
        buy(amount)
        price = round(list(data_frame.Close)[-1:][0], 2)
        while True:
            RSI, MACD, Signal, data_frame = main(amount)
            if round(list(data_frame.Close)[-1:][0], 2) > price + 0.1:
                gains = round(list(data_frame.Close)[-1:][0], 2) - price
                profits.append(gains)
                gains = sum(profits)
                sell(price, gains, 5)
                break
            time.sleep(15)
    time.sleep(15)
