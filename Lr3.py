import datetime
import pandas as pd
from binance.client import Client
import pandas_ta as ta

# Configuration
SYMBOL = "BTCUSDT"
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
N_DAYS_AGO = 1

def fetch_historical_data(symbol, interval, start_str, end_str):
    client = Client()
    klines = client.get_historical_klines(symbol, interval, start_str, end_str)
    columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_vol', 'trades', 'tb_base_vol', 'tb_quote_vol', 'ignore']
    df = pd.DataFrame(klines, columns=columns)
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    numeric_cols = ['open', 'high', 'low', 'close']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return df[['time', *numeric_cols]]

def calculate_indicators(df):
    # Applying technical indicators directly on the dataframe
    df['RSI'] = ta.rsi(df['close'])
    df['CCI'] = ta.cci(df['high'], df['low'], df['close'])
    df[['MACD', 'MACD_signal', 'MACD_hist']] = ta.macd(df['close'])
    return df.dropna()

def interpret_signals(row):
    signals = {
        'RSI': "перекупленість" if row["RSI"] > 70 else "перепроданість" if row["RSI"] < 30 else "нейтрально",
        'CCI': "можливий початок висхідного тренду" if row["CCI"] < -100 else "можливий початок низхідного тренду" if row["CCI"] > 100 else "нейтрально",
        'MACD': "бичачий перехрест" if row['MACD'] > row['MACD_signal'] else "ведмежий перехрест" if row['MACD'] < row['MACD_signal'] else "нейтрально"
    }
    # Returning the interpretation as a string
    return ', '.join([f"{key}: {value}" for key, value in signals.items()])

def main():
    start_date = (datetime.datetime.now() - datetime.timedelta(days=N_DAYS_AGO)).strftime('%Y-%m-%d %H:%M')
    end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    data = fetch_historical_data(SYMBOL, INTERVAL, start_date, end_date)
    data_with_indicators = calculate_indicators(data)
    data_with_indicators['Prediction'] = data_with_indicators.apply(interpret_signals, axis=1)
    data_with_indicators.to_csv('prediction.csv', index=False)
    print("Saved predictions to prediction.csv")

if __name__ == "__main__":
    main()
