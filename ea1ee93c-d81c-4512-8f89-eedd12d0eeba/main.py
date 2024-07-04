from surmount.base_class import Strategy, TargetAllocation

class TradingStrategy(Strategy):
    def __init__(self):
        # Choose NVDA as the ticker of interest for the strategy
        self.ticker = "NVDA"

    @property
    def assets(self):
        # Specify the assets we are interested in
        return [self.ticker]

    @property
    def interval(self):
        # Set the interval to daily, to run the strategy after the market closes each day
        return "1day"

    def run(self, data):
        # Implement the trading logic
        ohlcv_data = data["ohlcv"]
        allocation = {}

        # Check if there's enough historical data (at least 2 days) to compare
        if len(ohlcv_data) >= 2:
            # Get the daily low of today and yesterday for NVDA
            todays_low = ohlcv_dira[-1][self.ticker]["low"]
            yesterdays_low = ohlcv_data[-2][self.ticker]["low"]

            # If today's daily low is greater than 99.99% of yesterday's low, then sell NVDA
            if todays_low > yesterdays_low * 0.9999:
                allocation[self.ticker] = 0  # Sell all NVDA
            # If today's daily low is lower than 99.99% of yesterday's low, then buy NVDA
            elif todays_low < yesterdays_low * 0.9999:
                allocation[self.ticker] = 1  # Use 100% of current balance to buy NVDA
        else:
            # If there's not enough historical data, do nothing
            allocation[self.ticker] = 0  # Maintain current allocation

        # Return the target allocation
        return TargetAllocation(allocation)