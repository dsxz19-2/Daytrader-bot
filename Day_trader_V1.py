import time
import yfinance as yf
import datetime as dt
import ta
from datetime import datetime, timedelta 
import sys

def buy(budget):
    utc_now = datetime.utcnow()
    utc_now.strftime("%Y-%m-%d %I:%M")
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %I:%M")

    with open("orderV1.txt", "a") as f:
        f.write(f"\nBUY: {list(data_frame.Close)[-1:][0] * amount} \n"
                f"UTC Time: {utc_now} \n"
                f"Local Time: {now} \n"
                f"Budget: {budget - (list(data_frame.Close)[-1:][0] * amount)} \n")

def sell(buy_price, sum_of_profits, budget):
    utc_now = datetime.utcnow()
    utc_now.strftime("%Y-%m-%d %I:%M")
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %I:%M")

    with open("orderV1.txt", "a") as f:
        f.write(f"\nSELL: {list(data_frame.Close)[-1:][0]} \n"
                f"UTC Time: {utc_now} \n"
                f"Local Time: {now} \n"
                f"Budget: {budget} \n"
                f"Profit Of Trade: {list(data_frame.Close)[-1:][0] - buy_price} \n"
                f"Total Profits: {sum_of_profits} \n")
        f.close()
        profit = list(data_frame.Close)[-1:][0] - buy_price
        return profit

def main():
    end = dt.datetime.now()
    data = yf.download("SOL-CAD", start=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d'), end=end,
                       interval="5m")

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
    print("RSI:", round(rsi, 2))
    print("MACD:", round(macd, 2))
    print("Signal:", round(signal, 2))
    print("Close:", round(list(data.Close)[-1:][0], 2))
    return round(rsi, 2), round(macd, 2), round(signal, 2), data


trigger = 1
total_profits = []
paper_money = 1000000
amount = 10

while trigger == 1:
    RSI, MACD, Signal, data_frame = main()
    if (MACD > Signal) and (RSI > 50) and trigger == 1:
        buy(paper_money)
        price = round(list(data_frame.Close)[-1:][0], 2) * amount
        paper_money = paper_money - price
        trigger = -1
        while trigger == -1:
            time.sleep(10)
            RSI, MACD, Signal, data_frame = main()
            if ((price / amount) + .10) < (round(list(data_frame.Close)[-1:][0], 2)):
                gains = round(list(data_frame.Close)[-1:][0], 2) - price
                total_profits.append(gains)
                sell(price, sum(total_profits), paper_money)
                paper_money = paper_money + round(list(data_frame.Close)[-1:][0], 2) * amount
                trigger = 1
                break
    time.sleep(10)


