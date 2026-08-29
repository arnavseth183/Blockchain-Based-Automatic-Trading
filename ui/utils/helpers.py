import random
import pandas as pd

def fetch_market_data(symbol):

    price = random.uniform(1000, 3000)

    historical = pd.Series(
        [price + random.uniform(-10, 10) for _ in range(50)]
    )

    return {
        "symbol": symbol,
        "price": price,
        "historical": historical
    }

def validate_symbol(symbol):
    allowed = ["RELIANCE", "TCS", "INFY"]
    return symbol in allowed

def calculate_pnl(entry, current, qty):
    return (current - entry) * qty