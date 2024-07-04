from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["NVDA"]

    @property
    def interval(self):
        # Assuming '1day' interval data is provided after the market close each day
        return "1day"

    @property
    def assets(self):
        # Targeting only NVDA for this strategy
        return self.tickers

    def run(self, data):
        allocation_dict = {}
        
        # Getting NVDA's OHLCV data
        nvda_data = data["ohlcv"]["NVDA"]
        
        # Ensure there are at least 2 days of data to compare
        if len(nvda_data) > 1:
            # Getting the last two days of NVDA data
            today_low = nvda_data[-1]["low"]
            previous_day_low = nvda_data[-2]["low"]

            # If today's low is greater than 99.99% of the previous day's low, sell NVDA,
            # else, if today's low is lower, buy NVDA the next day at market open.
            if today_low > previous_day_low * 0.9999:
                allocation_dict["NVDA"] = 0  # Sell signal, no allocation
            else:
                allocation_dict["NVDA"] = 1  # Buy signal, full allocation
        else:
            # If not enough data, do not allocate
            allocation_dict["NVDA"] = 0

        return TargetAllocation(allocation_dict)