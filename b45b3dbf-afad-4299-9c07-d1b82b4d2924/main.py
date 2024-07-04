from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        return ["NVDA"]

    @property
    def interval(self):
        # Specifies the interval at which the strategy runs, set to daily close.
        return "1day"

    def run(self, data):
        # Implementation of the strategy that decides to buy or sell NVDA based on the comparison of daily lows.
        
        # Initialize the target allocation with no change (keep current positions).
        allocation = {}
        
        # Check if there are at least two days of data to compare the lows.
        if len(data["ohlcv"]) > 1:
            # Get the last two days of NVDA data.
            current_day_data = data["ohlcv"][-1]["NVDA"]
            previous_day_data = data["ohlcv"][-2]["NVDA"]
            
            # Compare the lows of the last two days.
            if current_day_data["low"] > previous_day_data["low"]:
                # If today's low is greater than yesterday's, sell all NVDA by setting its target allocation to 0.
                log("Selling NVDA - today's low is greater than yesterday's low")
                allocation["NVDA"] = 0
            elif current_day_data["low"] < previous_day_data["low"]:
                # If today's low is lower than yesterday's, buy NVDA with all available balance by setting its target allocation to 1.
                log("Buying NVDA - today's low is lower than yesterday's low")
                allocation["NVDA"] = 1
            else:
                # If today's low is the same as yesterday's, make no change.
                log("No change - today's low is equal to yesterday's low")
        else:
            # If there is not enough data, log a message and make no allocation change.
            log("Not enough data to make a decision")
        
        return TargetAllocation(allocation)