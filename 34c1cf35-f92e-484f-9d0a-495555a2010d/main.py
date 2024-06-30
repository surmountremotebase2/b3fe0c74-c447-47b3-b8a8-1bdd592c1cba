import pandas as pd
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest, TakeProfitDetails, StopLossDetails
from oanda_candles import Pair, Gran, CandleClient  # Ensure this package is available or replace with an alternative
from config import access_token, accountID  # Ensure your config file is properly set up
from apscheduler.schedulers.blocking import BlockingScheduler

# Function to generate trading signals
def signal_generator(df):
    open_price = df['Open'].iloc[-1]
    close_price = df['Close'].iloc[-1]
    previous_open = df['Open'].iloc[-2]
    previous_close = df['Close'].iloc[-2]

    # Bearish Pattern
    if (open_price > close_price and
        previous_open < previous_close and
        close_price < previous_open and
        open_price >= previous_close):
        return 1

    # Bullish Pattern
    elif (open_price < close_price and
          previous_open > previous_close and
          close_price > previous_open and
          open_price <= previous_close):
        return 2

    # No clear pattern
    else:
        return 0

# Function to retrieve candlestick data
def get_candles(n):
    client = CandleClient(access_token, real=False)
    collector = client.get_collector(Pair.EUR_USD, Gran.M15)
    candles = collector.grab(n)
    return candles

# Function to fetch historical data (replace this with your data fetching method)
def get_historical_data():
    # Example: Generate synthetic data or fetch from an alternative source
    data = {
        'Open': [1.10, 1.12, 1.15, 1.13, 1.14],
        'Close': [1.11, 1.13, 1.16, 1.14, 1.15],
        'High': [1.12, 1.14, 1.17, 1.15, 1.16],
        'Low': [1.09, 1.11, 1.14, 1.12, 1.13]
    }
    df = pd.DataFrame(data)
    return df

# Function to execute trading logic
def trading_job():
    # Generate signals based on historical data
    dataF = get_historical_data()

    signals = []
    for i in range(1, len(dataF)):
        df = dataF[i-1:i+1]
        signal = signal_generator(df)
        signals.append(signal)
    
    dataF["signal"] = [0] + signals  # Adding initial signal as 0
    
    # Example of executing orders
    client = API(access_token)
    SLTPRatio = 2.0
    candles = get_candles(3)  # Get candlestick data

    # Process candlestick data into DataFrame
    dfstream = pd.DataFrame(columns=['Open', 'Close', 'High', 'Low'])
    for i, candle in enumerate(candles):
        dfstream.loc[i, 'Open'] = float(str(candle.bid.o))
        dfstream.loc[i, 'Close'] = float(str(candle.bid.c))
        dfstream.loc[i, 'High'] = float(str(candle.bid.h))
        dfstream.loc[i, 'Low'] = float(str(candle.bid.l))

    dfstream = dfstream.astype(float)
    signal = signal_generator(dfstream.iloc[:-1, :])  # Generate signal based on historical data

    previous_candle_range = abs(dfstream['High'].iloc[-2] - dfstream['Low'].iloc[-2])

    SLBuy = float(str(candle.bid.o)) - previous_candle_range
    SLSell = float(str(candle.bid.o)) + previous_candle_range

    TPBuy = float(str(candle.bid.o)) + previous_candle_range * SLTPRatio
    TPSell = float(str(candle.bid.o)) - previous_candle_range * SLTPRatio

    # Example of placing orders based on signal
    if signal == 1:
        mo = MarketOrderRequest(instrument="EUR_USD", units=-1000,
                                takeProfitOnFill=TakeProfitDetails(price=TPSell).data,
                                stopLossOnFill=StopLossDetails(price=SLSell).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)
    elif signal == 2:
        mo = MarketOrderRequest(instrument="EUR_USD", units=1000,
                                takeProfitOnFill=TakeProfitDetails(price=TPBuy).data,
                                stopLossOnFill=StopLossDetails(price=SLBuy).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)

# Execute the trading job
trading_job()

# Example of scheduling the trading job (uncomment and adjust as needed)
# scheduler = BlockingScheduler()
# scheduler.add_job(trading_job, 'cron', day_of_week='mon-fri', hour='00-23', minute='1,16,31,46', start_date='2022-01-12 12:00:00', timezone='America/Chicago')
# scheduler.start()