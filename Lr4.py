import pandas as pd
from ta.momentum import RSIIndicator
import matplotlib.pyplot as plt
from binance import Client

def fetch_historical_data(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1 day ago UTC", end_str="now UTC"):
    client = Client()
    k_lines = client.get_historical_klines(symbol, interval, start_str, end_str)
    columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    df = pd.DataFrame(k_lines, columns=columns)
    df[['Time', 'Open', 'High', 'Low', 'Close']] = df[['Time', 'Open', 'High', 'Low', 'Close']].apply(pd.to_numeric, errors='coerce')
    df['Time'] = pd.to_datetime(df['Time'], unit='ms')
    return df

def calculate_rsi(df, periods=[14]):
    for period in periods:
        indicator_rsi = RSIIndicator(df['Close'], window=period)
        df[f'RSI_{period}'] = indicator_rsi.rsi()
    return df

def plot_data(df, periods=[14]):
    plt.figure(figsize=(14, 7 * len(periods)))

    # Plotting close price
    ax1 = plt.subplot(len(periods) + 1, 1, 1)
    df.plot(x='Time', y='Close', ax=ax1, title="Close Price", legend=False)
    ax1.set_ylabel('Price')

    # Plotting RSI for each period in a new subplot
    for i, period in enumerate(periods, start=2):
        ax = plt.subplot(len(periods) + 1, 1, i, sharex=ax1)
        df.plot(x='Time', y=f'RSI_{period}', ax=ax, title=f"RSI for {period} periods", legend=False)
        ax.set_ylim([0, 100])  # RSI ranges from 0 to 100
        ax.axhline(70, color="red", linestyle="--")
        ax.axhline(30, color="green", linestyle="--")
        ax.set_ylabel('RSI Value')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    data = fetch_historical_data()
    periods = [14, 27, 100]
    data_with_rsi = calculate_rsi(data, periods=periods)
    plot_data(data_with_rsi, periods=periods)
