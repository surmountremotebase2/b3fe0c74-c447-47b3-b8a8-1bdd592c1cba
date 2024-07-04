from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "NVDA"
        # OHLCV data for NVDA will be used for analysis
        self.data_list = [OHLCV(self.ticker)]

    @property
    def interval(self):
        # The strategy is designed to run after the market close of each day.
        return "1day"

    @property
    def assets(self):
        # NVDA is the asset of interest.
        return [self.ticker]

    @property
    def data(self):
        # Data required for the strategy is defined in the __init__ method.
        return self.data_list

    def run(self, data):
        # Initialize target allocation with no position as the default.
        allocation_dict = {self.ticker: 0}

        # Ensure there is enough data to compare current and previous day's lows.
        if len(data["ohlcv"]) > 1:
            # Retrieve the last two days of data.
            today_data = data["ohlcv"][-1][self.ticker]
            yesterday_data = data["ohlcv"][-2][self.ticker]

            # Check if today's low is greater than yesterday's low * 0.9999.
            if today_data["low"] > (yesterday_data["low"] * 0.9999):
                # Selling NVDA (setting allocation to 0 signifies selling).
                log("Selling NVDA - Daily low increased.")
                allocation_dict[self.ticker] = 0
            else:
                # Buying NVDA at next day's market open (allocating full position).
                # Here we assume full allocation is represented by 1.
                log("Buying NVDA - Daily low decreased.")
                allocation_dict[self.ticker] = 1

        # Return the target allocation based on the analysis.
        return TargetAllocation(allocation_dict)