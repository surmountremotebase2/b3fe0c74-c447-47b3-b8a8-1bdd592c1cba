from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership
import yfinance as yf
import pandas as pd

# Download data from Yahoo Finance
dataF = yf.download("EURUSD=X", start="2022-10-7", end="2022-12-5", interval='15m')
print(dataF.iloc[:,:])

def signal_generator(df):
    open = df.Open.iloc[-1]
    close = df.Close.iloc[-1]
    previous_open = df.Open.iloc[-2]
    previous_close = df.Close.iloc[-2]

    # Bearish Pattern
    if (open > close and
        previous_open < previous_close and
        close < previous_open and
        open >= previous_close):
        return 1

    # Bullish Pattern
    elif (open < close and
          previous_open > previous_close and
          close > previous_open and
          open <= previous_close):
        return 2

    # No clear pattern
    else:
        return 0

signal = [0]
for i in range(1, len(dataF)):
    df = dataF[i-1:i+1]
    signal.append(signal_generator(df))

dataF["signal"] = signal
print(dataF.signal.value_counts())

# Imports needed for trading (continue from your Jupyter Notebook setup)
from apscheduler.schedulers.blocking import BlockingScheduler
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oanda_candles import Pair, Gran, CandleClient
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from config import access_token, accountID  # Ensure your config file is properly set up

# Define function to get candles
def get_candles(n):
    client = CandleClient(access_token, real=False)
    collector = client.get_collector(Pair.EUR_USD, Gran.M15)
    candles = collector.grab(n)
    return candles

# Function to process trading logic
def trading_job():
    candles = get_candles(3)
    dfstream = pd.DataFrame(columns=['Open','Close','High','Low'])

    i = 0
    for candle in candles:
        dfstream.loc[i, 'Open'] = float(str(candle.bid.o))
        dfstream.loc[i, 'Close'] = float(str(candle.bid.c))
        dfstream.loc[i, 'High'] = float(str(candle.bid.h))
        dfstream.loc[i, 'Low'] = float(str(candle.bid.l))
        i += 1

    dfstream = dfstream.astype(float)
    signal = signal_generator(dfstream.iloc[:-1, :])

    # Example of executing orders
    client = API(access_token)
    SLTPRatio = 2.0
    previous_candleR = abs(dfstream['High'].iloc[-2] - dfstream['Low'].iloc[-2])

    SLBuy = float(str(candle.bid.o)) - previous_candleR
    SLSell = float(str(candle.bid.o)) + previous_candleR

    TPBuy = float(str(candle.bid.o)) + previous_candleR * SLTPRatio
    TPSell = float(str(candle.bid.o)) - previous_candleR * SLTPRatio

    print(dfstream.iloc[:-1, :])
    print(TPBuy, "  ", SLBuy, "  ", TPSell, "  ", SLSell)

    # Example of placing orders based on signal
    if signal == 1:
        mo = MarketOrderRequest(instrument="EUR_USD", units=-1000, takeProfitOnFill=TakeProfitDetails(price=TPSell).data, stopLossOnFill=StopLossDetails(price=SLSell).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)
    elif signal == 2:
        mo = MarketOrderRequest(instrument="EUR_USD", units=1000, takeProfitOnFill=TakeProfitDetails(price=TPBuy).data, stopLossOnFill=StopLossDetails(price=SLBuy).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)

# Execute the trading job
trading_job()

# Example of scheduling the trading job (uncomment and adjust as needed)
# scheduler = BlockingScheduler()
# scheduler.add_job(trading_job, 'cron', day_of_week='mon-fri', hour='00-23', minute='1,16,31,46', start_date='2022-01-12 12:00:00', timezone='America/Chicago')
# scheduler.start()