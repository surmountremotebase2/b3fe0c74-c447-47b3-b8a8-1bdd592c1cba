from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership
import pandas_ta as ta
import pandas as pd
from datetime import datetime, timedelta

class TradingStrategy(Strategy):
    def init(self):
        self.tickers = ["VIRT"]
        self.data_list = []
        self.last_trade_action = None  # To track the last trade action

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
        vols = [i["VIRT"]["volume"] for i in data["ohlcv"]]
        smavols = self.SMAVol("VIRT", data["ohlcv"], 30)
        smavols2 = self.SMAVol("VIRT", data["ohlcv"], 10)

        if len(vols) <= 4:
            return TargetAllocation({})

        try:
            last_day_data = data["ohlcv"][-2]  # Data for the last trading day
            last_open = last_day_data["VIRT"]["open"]
            last_close = last_day_data["VIRT"]["close"]

            # Check condition 1: Closing price of last day < 98.42% of opening price of same day
            condition1 = (last_close < 0.9842 * last_open)

            # Calculate day market change
            day_market_change = (last_close / data["ohlcv"][-6]["VIRT"]["close"]) - 1  # 5 days prior

            # Check condition 2: Day market change of 5 days ago > day market change of last day
            condition2 = (day_market_change > (last_close / data["ohlcv"][-3]["VIRT"]["close"]) - 1)  # Last day

            if condition1 or condition2:
                # Buy at market open of the next day
                self.last_trade_action = 'buy'
                return TargetAllocation({"VIRT": 1.0})  # Allocate 100% of portfolio to buy
            else:
                # Sell at market open of the next day
                self.last_trade_action = 'sell'
                return TargetAllocation({"VIRT": -1.0})  # Sell all shares
        except Exception as e:
            log.error(f"Error running strategy: {e}")
            return TargetAllocation({})

    def SMAVol(self, ticker, data, length):
        """
        Calculate the moving average of trading volume.

        :param ticker: a string ticker
        :param data: data as provided from the OHLCV data function
        :param length: the window
        :return: list with float SMA
        """
        close = [i[ticker]["volume"] for i in data]
        d = ta.sma(pd.Series(close), length=length)
        if d is None:
            return []
        return d.tolist()

    def before_trading_starts(self):
        """
        Place market order at market open of the next trading day based on last recorded trade action.
        """
        if self.last_trade_action:
            try:
                # Get tomorrow's date
                tomorrow = datetime.now().date() + timedelta(days=1)

                # Place market order based on last trade action
                if self.last_trade_action == 'buy':
                    self.api.submit_order(
                        symbol="VIRT",
                        qty=1,  # Adjust quantity as per your strategy
                        side='buy',
                        type='market',
                        time_in_force='opg'
                    )
                    log.info(f"Buy order placed for VIRT at market open on {tomorrow}.")
                elif self.last_trade_action == 'sell':
                    self.api.submit_order(
                        symbol="VIRT",
                        qty=1,  # Adjust quantity as per your strategy
                        side='sell',
                        type='market',
                        time_in_force='opg'
                    )
                    log.info(f"Sell order placed for VIRT at market open on {tomorrow}.")
            except Exception as e:
                log.error(f"Error placing market order: {e}")

        else:
            log.warning("No valid last trade action recorded.")