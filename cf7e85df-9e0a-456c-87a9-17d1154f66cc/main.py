from surmount.base_class import Strategy, TargetAllocation

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker of interest
        self.ticker = "NVDA"
        self.data_list = []

    @property
    def assets(self):
        # Define which assets this strategy is interested in
        return [self.ticker]

    @property
    def interval(self):
        # Run this strategy at the end of the day for daily data
        return "1day"

    @property
    def data(self):
        # No additional data feeds required for this strategy
        return self.data_list

    def run(self, data):
        # Initialize NVDA allocation to 0 (no position change by default)
        nvda_allocation = 0

        # Access OHLCV data for NVDA from the provided data dictionary
        ohlcv_data = data["ohlcv"]

        # Check if we have at least two days of data to make a comparison
        if len(ohlcv_data) >= 2:
            # Fetch the low prices for the last two days
            today_low = ohlcv_data[-1][self.ticker]["low"]
            yesterday_low = ohlcv_data[-2][self.ticker]["low"]

            # Strategy logic
            if today_low > yesterday_low * 0.9999:
                # If today's low is greater than 99.99% of yesterday's low, indicate to sell
                # Setting allocation to 0 to indicate selling off the position
                nvda_allocation = 0
            else:
                # If today's low is less than or equal to 99.99% of yesterday's low, indicate to buy
                # Setting allocation to 1 to go long the entire portfolio in NVDA
                nvda_allocation = 1

        # Return the target allocation
        return TargetAllocation({self.ticker: nvda_allocation})