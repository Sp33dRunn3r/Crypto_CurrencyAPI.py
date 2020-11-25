from binance.client import Client
from datetime import datetime
from pandas import DataFrame as df
import Keys
import pandas as pd
import numpy as np
from scipy.stats import norm


def binance_price():
    client = Client(api_key=Keys.Pkey, api_secret=Keys.Skey)
    # LiteCoin to Tether
    candles = client.get_klines(symbol='LTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE)

    candles_data_frame = df(candles)
    candles_data_frame_date = candles_data_frame[0]

    final_date = []

    for time in candles_data_frame_date.unique():
        redable = datetime.fromtimestamp(int(time/1000))
        final_date.append(redable)

    initial_investment = 10000
    candles_data_frame.pop(0)
    candles_data_frame.pop(11)
    dataframe_final_date = df(final_date)
    dataframe_final_date.columns = ['date']
    final_data_frame = candles_data_frame.join(dataframe_final_date)
    final_data_frame.set_index('date', inplace=True)
    final_data_frame.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Close_Time', 'Quote_asset_volume', 'Number_of_trades', 'Taker_buy_base', 'Taker_buy_quote']
    final_data_frame.to_csv('Binance_report1.csv')
    data = pd.read_csv('Binance_report1.csv')
    data['Daily_return_log'] = np.log(data['Close'] / data['Close'].shift(1))
    data.to_csv('final_report1.csv', mode='a', header=True)
    print(data)
    return final_data_frame

print(binance_price())