from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership
import pandas_ta as ta
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["NVDA"]
        self.data_list = []

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        closing_prices = [i["NVDA"]["close"] for i in data["ohlcv"]]
        opening_prices = [i["NVDA"]["open"] for i in data["ohlcv"]]

        if len(closing_prices) < 2:
            return TargetAllocation({})

        last_day_closing_price = closing_prices[-2]
        last_day_opening_price = opening_prices[-2]

        if last_day_closing_price > last_day_opening_price:
            action = "BUY"  # Buy if closing price is higher than opening price
        else:
            action = "SELL"  # Sell if closing price is lower than opening price

        log.info(f"Action to take at market open of the next day: {action}")

        # Return an empty TargetAllocation for this example
        return TargetAllocation({})