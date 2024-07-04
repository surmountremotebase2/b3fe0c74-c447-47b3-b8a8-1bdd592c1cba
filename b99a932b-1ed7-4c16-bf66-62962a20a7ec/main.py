from surmount.base_class import Strategy, TargetAllocation
from surmuch.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker of interest for the strategy
        self.ticker = "NVDA"

    @property
    def assets(self):
        # Define which assets this strategy is interested in
        return [self.ticker]

    @property
    def interval(self):
        # The strategy operates on a daily interval, checking after each market close
        return "1day"

    def run(self, data):
        # Initialize the desired allocation as an empty dictionary
        allocation = {}

        # Retrieve the OHLCV (Open/High/Low/Close/Volume) data for NVDA
        ohlcv_data = data["ohlcv"]

        # Ensure there are at least two days of data to compare
        if len(ohlcv_data) >= 2:
            # Get the daily lows for the last two days
            current_day_low = ohlcv_data[-1][self.ticker]["low"]
            previous_day_low = ohlcv_data[-2][self.ticker]["low"]

            # Check if today's low is greater than 99.99% of yesterday's low
            if current_day_low > previous_day_low * 0.9999:
                # If true, sell all holdings of NVDA
                allocation[self.ticker] = 0
            else:
                # If today's low is lower, allocate all available cash to buy NVDA at the next open
                # Here we simulate this by setting allocation to 1, indicating full allocation towards NVDA.
                # Note: The actual implementation of using all available cash to buy NVDA should be handled 
                # by the trading system based on account balance, not directly in the strategy.
                allocation[self.ticker] = 1
        else:
            # Log an info message if there's not enough data
            log("Not enough data to execute strategy")

        # Return the target allocation. If no condition was met, the allocation remains empty
        return TargetImplementation(allocation)