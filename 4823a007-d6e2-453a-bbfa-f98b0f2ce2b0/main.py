from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "NVDA"
        self.shares_to_trade = 40

    @property
    def interval(self):
        # This strategy runs after market close of each day.
        return "1day"

    @property
    def assets(self):
        # Only interested in NVDA for this strategy.
        return [self.ticker]
    
    @property
    def data(self):
        # No additional data needed from surmount.data
        return []

    def run(self, data):
        ohlcv = data["ohlcv"]  # Access the open-high-low-close-volume data for the assets.
        
        # Check if we have at least two days of data to compare current and previous day's lows.
        if len(ohlcv) >= 2:
            current_day_low = ohlcv[-1][self.ticker]["low"]
            previous_day_low = ohlcv[-2][self.ticker]["low"]

            # If today's low is greater than 99.99% of yesterday's low, plan to sell 40 shares.
            if current_day_low > previous_day_low * 0.9999:
                allocation = {"NVDA": -self.shares_to_trade}  # Negative for selling
                log(f"Planning to sell {self.shares_to_trade} shares of {self.ticker}")

            # If today's low is lower than 99.99% of yesterday's low, plan to buy 40 shares.
            elif current_day_low < previous_day_low * 0.9999:
                allocation = {"NVDA": self.shares_to_trade}  # Positive for buying
                log(f"Planning to buy {self.shares_to_trade} shares of {self.ticker}")

            else:
                # No trade if the conditions don't meet.
                allocation = {}
                log("No trading action for today.")
        else:
            # Not enough data to make a decision.
            allocation = {}
            log("Not enough data to compare daily lows for NVDA.")

        # Return the TargetAllocation object with our trading plans.
        # Note: Actual trading of specific quantities cannot be directly represented using TargetAllocation.
        # The allocation values need to be interpreted accordingly in the live trading logic by the user.
        return TargetAllocation(allocation)