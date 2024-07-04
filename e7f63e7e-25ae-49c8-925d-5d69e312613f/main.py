from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, OHLCV

class TradingStrategy(Strategy):

    def __init__(self):
        self.ticker = "NVDA"
        self.data_list = [OHLCV(self.ticker)]

    @property
    def interval(self):
        # This strategy checks signals after the closing of each day.
        return "1day"

    @property
    def assets(self):
        # This strategy focuses on trading NVDA.
        return [self.ticker]

    @property
    def data(self):
        # Data requirements for this strategy include OHLCV data for NVDA.
        return self.data_list

    def run(self, data):
        ohlcv = data["ohlcv"][self.ticker]
        
        # Initializing the target allocation for NVDA to 0 (meaning sell all or stay out)
        nvda_stake = 0

        # Check if we have at least 2 days of data to compare today's low with yesterday's low
        if len(ohlcv) >= 2:
            today_low = ohlcv[-1]["low"]
            yesterday_low = ohlcv[-2]["low"]

            # If today's low is greater than 99.99% of yesterday's low, set the NVDA stake accordingly
            if today_low > yesterday_low * 0.9999:
                # Signal to buy NVDA - allocate 100% of available account balance to NVDA
                nvda_stake = 1
            else:
                # Signal to sell NVDA - allocate 0% of available account balance to NVDA
                nvda_stake = 0

        # Creating a TargetAllocation object with the NVDA stake
        # If nvda_stake is 1, it means buy or hold NVDA based on available account balance
        # If nvda_stake is 0, it means sell all NVDA holdings
        return TargetAllocation({self.ticker: nvda_stake})