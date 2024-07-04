from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["NVDA"]
        self.previous_day_low = None  # Initialize without a previous day low

    @property
    def interval(self):
        # Specifies the frequency of data to be daily, as strategy checks after market close
        return "1day"

    @property
    def assets(self):
        # Specifies the assets this strategy is interested in, which is NVDA
        return self.tickers

    @property
    def data(self):
        # No additional data requirement specified for this strategy
        return []

    def run(self, data):
        # Initialize allocation with no position
        allocation_dict = {"NVDA": 0}

        # Retrieve the OHLCV data for NVDA
        ohlcv = data["ohlcv"]
        if len(ohlcv) < 2:
            # Not enough data to make a decision yet
            return TargetAllocation(allocation_dict)

        # Get the daily low for the current and previous day
        current_day_low = ohlcv[-1]["NVDA"]["low"]
        previous_day_low = ohlcv[-2]["NVDA"]["low"]

        # Check if the current day's low is greater than the previous day's low * 0.9999
        if current_day_low > (previous_day_low * 0.9999):
            log("Sell all NVDA - daily low increased compared to the previous day.")
            allocation_dict["NVDA"] = 0  # Indicate to sell all NVDA
        else:
            log("Buy NVDA - daily low decreased compared to the previous day.")
            # Indicate to buy NVDA with all available account balance at next market open
            # However, TargetAllocation cannot directly specify to "buy with all available balance".
            # Instead, set an indicative target allocation for NVDA. The actual implementation
            # of using all available account balance to buy NVDA should be handled based on the account,
            # current position, and this signal by the trading logic interfacing with the brokerage.
            allocation_dict["NVDA"] = 1  # Indicate desire to allocate fully towards NVDA
        
        # Update previous day low for the next run
        self.previous_day_low = current_day_low

        return TargetAllocation(allocation_dict)