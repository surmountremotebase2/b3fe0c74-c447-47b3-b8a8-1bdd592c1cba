from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Specify the ticker symbol of the asset you're interested in
        self.ticker = "AAPL"

    @property
    def assets(self):
        # This strategy is concerned with a single asset
        return [self.ticker]

    @property
    def interval(self):
        # Use daily data to check for the price changes
        return "1day"

    def run(self, data):
        # Access the historical close prices for the asset.
        # Assume 'ohlcv' provides a dictionary structured as {ticker: {"close": [price list]}}
        # with data sorted from oldest to newest.
        close_prices = data["ohlcv"][self.ticker]["close"]

        if len(close_prices) >= 3:
            # Calculate the price changes over the last two days.
            delta_yesterday = close_prices[-2] - close_prices[-3]
            delta_day_before_yesterday = close_prices[-3] - close_prices[-4]

            # If both price changes were negative, set allocation to buy (1.0 for fully allocated),
            # else sell (0.0 indicates no allocation for the asset, simulating a sell action).
            if delta_yesterday < 0 and delta_day_before_yesterday < 0:
                allocation_dict = {self.ticker: 1.0}
            else:
                allocation_dict = {self.ticker: 0.0}
        else:
            # In case there's not enough data to determine the price trend, no allocation is made.
            allocation_dict = {self.ticker: 0.0}
        
        return TargetAllocation(allocation_dict)