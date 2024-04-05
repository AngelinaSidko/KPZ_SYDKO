import pandas as pd
from binance.client import Client


def get_historical_data(symbol, start_str, end_str, interval='1m'):
    client = Client()
    interval_map = {
        '1m': Client.KLINE_INTERVAL_1MINUTE,
        # Можна додати більше відображень для інших інтервалів
    }
    klines = client.get_historical_klines(symbol, interval_map.get(interval, interval), start_str, end_str)

    columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
               'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
               'taker_buy_quote_asset_volume', 'ignore']

    data = pd.DataFrame(klines, columns=columns)
    numeric_columns = ['open', 'high', 'low', 'close', 'volume']
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
    data['time'] = pd.to_datetime(data['time'], unit='ms')

    return data


def calculate_RSI(dataframe, period=14):
    delta = dataframe['close'].diff()
    gain = (delta > 0) * delta
    loss = (delta < 0) * -delta

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    dataframe[f'RSI_{period}'] = rsi

    return dataframe[['time', f'RSI_{period}']]


# Використання коду
symbol = 'BTCUSDT'
start_time = (pd.Timestamp.now() - pd.Timedelta(days=1)).strftime('%Y-%m-%d %H:%M')
end_time = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')

data = get_historical_data(symbol, start_time, end_time)
rsi_data = calculate_RSI(data, period=14)

print(rsi_data.tail())
