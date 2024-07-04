from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "NVDA"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # Run the strategy after the market close of each day
        return "1day"

    def run(self, data):
        # Extract OHLCV data for NVDA
        d = data["ohlcv"]

        # Initialize NVDA allocation to 0 (indicating no action by default)
        nvda_stake = 0

        # Check if we have at least two days' data to compare current and previous lows
        if len(d) > 1:
            # Access yesterday's and today's low prices for NVDA
            yesterday_low = d[-2][self.ticker]["low"]
            today_low = d[-1][self.ticker]["low"]

            # Compare today's low with yesterday's low * 0.9999
            if today_low > yesterday_low * 0.9999:
                log("Selling NVDA")
                # Strategy to sell: Assign NVDA stake to 0, indicating liquidation/sell
                nvda_stake = 0
            elif today_low < yesterday_low * 0.9999:
                log("Buying NVDA")
                # Strategy to buy: Assign NVDA stake to 1, indicating full investment/buy
                nvda_stake = 1

        # Return the target allocation
        return Target