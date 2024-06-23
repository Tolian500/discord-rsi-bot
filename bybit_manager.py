import os
import time
import json
from datetime import datetime
import ta
import pandas as pd

import pybit
from pybit.unified_trading import HTTP

API_KEY = os.environ["bybit-api-key"]
API_SECRET = os.environ["bybit-api-secret"]

# Initialize the session
session = HTTP(
    testnet=False,
    api_key=API_KEY,
    api_secret=API_SECRET,
)

# Parameters for the K-line data
symbol = "SOLUSDT"
interval = "60"  # Use "1" for 1-minute interval; other possible values: "3", "5", "15", "30", "60", "240", "1440" (in minutes)
start_time = int((time.time() - 60 * 60 * 24) * 1000)  # 24 hours ago in milliseconds
end_time = int(time.time() * 1000)  # current time in milliseconds

# Fetch spot K-line data for SOL/USDT
try:
    response = session.get_kline(
        category="spot",
        symbol=symbol,
        interval=interval,
        start=start_time,
        end=end_time,
        limit=200  # maximum number of K-lines to fetch
    )

    print("Full Response:", response)  # Print full response for inspection

    if response['retCode'] == 0:
        kline_data = response['result']['list']
        # RSI CALCULATION:
        df = pd.DataFrame(kline_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'other'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert milliseconds to datetime
        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(
            float)

        # Set timestamp as index
        df.set_index('timestamp', inplace=True)

        # Calculate RSI
        df['RSI'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()

        # Print the DataFrame with RSI
        print(df)

        # Sample explanation
        print(f"K-line data for {symbol}:")
        for item in kline_data[:1]:
            timestamp, open_price, high_price, low_price, close_price, volume, turnover = item
            timestamp = int(timestamp)
            dt_object = datetime.fromtimestamp(timestamp / 1000)
            print(f"Timestamp: {timestamp} (time: {dt_object}) , Open: {open_price}, High: {high_price}, Low: {low_price}, Close: {close_price}, Volume: {volume}, Turnover: {turnover}")





    else:
        print(f"Error fetching K-line data: {response['retMsg']}")
except pybit.exceptions.FailedRequestError as e:
    print(f"FailedRequestError: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")


