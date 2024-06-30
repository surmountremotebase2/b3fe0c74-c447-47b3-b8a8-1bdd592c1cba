from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"  # Example: Trading Apple stocks

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"  # Daily historical data

    def run(self, data):
        ohlcv = data["ohlcv"]
        should_buy = False

        # Check if we have at least 6 days of data (5 days prior + last day)
        if len(ohlcv) > 5:
            last_day = ohlcv[-1][self.ticker]
            five_days_ago = ohlcv[-6][self.ticker]

            # Closing price less than 98.42% of opening price condition
            if last_day["close"] < last_day["open"] * 0.9842:
                should_buy = True
            else:
                # Day market change 5 days ago vs last day
                five_days_ago_change = five_days_ago["close"] - five_days_ago["open"]
                last_day_change = last_standard = last_day["close"] - last_day["open"]

                if abs(five_days_ago_change) > abs(last_day_change):
                    should_buy = True

        # Calculate the target allocation
        allocation_pct = 1 if should_buy else -1  # Buy if condition met, otherwise sell

        log(f"Setting target allocation for {self.ticker}: {'Buy' if should_buy else 'Sell'} at next market open.")
        return TargetAllocation({self.ticker: allocation_pct})

        # Note: Implementation assumes the platform allows specifying the buy/sell action for the next market open
        # and can handle negative allocation (-1) as an instruction to sell. Adjustments may be required based on platform specifics.