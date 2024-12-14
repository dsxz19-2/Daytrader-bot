import time
import yfinance as yf
import datetime as dt
import ta
from datetime import datetime, timedelta
import ta


def calculate_bollinger_bands(df, length, mult):
    basis = df['Close'].rolling(window=length).mean()
    dev = mult * df['Close'].rolling(window=length).std()

    df['upper_band'] = basis + dev
    df['lower_band'] = basis - dev

    return df


def calculate_rsi(df, length):
    df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=length).rsi()
    return df


def main():
    end = dt.datetime.now()
    data = yf.download("BTC-CAD", start=datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d'), end=end,
                       interval="1h")
    data.reset_index(inplace=True)

    length = 30
    mult = 2.0
    rsi_length = 14
    rsi_overbought = 70
    rsi_oversold = 30

    # Calculate Bollinger Bands
    data = calculate_bollinger_bands(data, length, mult)

    # Calculate RSI
    data = calculate_rsi(data, rsi_length)

    positions = []

    for i in range(len(data)):
        row = data.iloc[i]

        if row['Close'] < row['upper_band']:
            positions.append(('Short', row['Datetime'], row['Close']))

        if row['Close'] > row['lower_band']:
            positions.append(('Long', row['Datetime'], row['Close']))

    for position in positions:
        trade_type, date, price = position
        print(f"Trade: {trade_type} - Date: {date} - Price: {price}")


if __name__ == "__main__":
    main()
