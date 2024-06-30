from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "NVDA"  # Example: Trading Apple stocks

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
            five_days_ago = ohlcv[-5][self.ticker]

            # Closing price less than 98.42% of opening price condition
            if last_day["close"] < last_day["open"] * 0.9842:
                should_buy = True
            else:
                # Day market change 5 days ago vs last day
                five_days_ago_change = five_days_ago["close"] - five_days_ago["open"]
                last_day_change = last_day["close"] - last_day["open"]

                if abs(five_days_ago_change) > abs(last_day_change):
                    should_buy = True

        # Calculate the target allocation
        allocation_pct = 1 if should_buy else 0  # Changed to 0 instead of -1

        log(f"Setting target allocation for {self.ticker}: {'Buy' if should_buy else 'Sell'} at next market open.")
        return TargetAllocation({self.ticker: allocation_pct})

        # Note: Implementation assumes the platform allows specifying the buy/sell action for the next market open
        # and can handle negative allocation (-1) as an instruction to sell. Adjustments may be required based on platform specifics.

# Example usage (if running outside of Surmount environment, you need to simulate data)
if __name__ == "__main__":
    # Simulated data format similar to what your Surmount environment provides
    sample_data = {
        "ohlcv": [
            {"NVDA": {"open": 150.0, "high": 155.0, "low": 148.0, "close": 152.0}},
            {"NVDA": {"open": 152.5, "high": 154.0, "low": 149.5, "close": 151.0}},
            {"NVDA": {"open": 151.0, "high": 153.0, "low": 148.0, "close": 150.0}},
            {"NVDA": {"open": 150.5, "high": 153.5, "low": 149.0, "close": 152.0}},
            {"NVDA": {"open": 152.0, "high": 156.0, "low": 151.0, "close": 154.0}},
            {"NVDA": {"open": 154.5, "high": 157.0, "low": 152.5, "close": 155.0}},
            {"NVDA": {"open": 155.0, "high": 157.5, "low": 153.0, "close": 156.0}},
        ]
    }

    strategy = TradingStrategy()
    strategy.run(sample_data)