import yfinance as yf


def get_live_price(symbol):
    try:
        ticker = yf.Ticker(symbol)

        # -------------------------------
        # 1. Try LIVE intraday price
        # -------------------------------
        data = ticker.history(period="1d", interval="1m")

        if not data.empty:
            return float(data["Close"].iloc[-1])

        # -------------------------------
        # 2. FALLBACK (market closed)
        # -------------------------------
        data = ticker.history(period="5d")

        if not data.empty:
            return float(data["Close"].iloc[-1])

        # -------------------------------
        # 3. FINAL FAILSAFE
        # -------------------------------
        return 0.0

    except Exception as e:
        print("Price fetch error:", e)
        return 0.0