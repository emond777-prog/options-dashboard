import yfinance as yf
import pandas as pd

def market_trend():
    try:
        df = yf.download("SPY", period="6mo", interval="1d")

        # Safety checks
        if df is None or df.empty:
            return "UNKNOWN"

        if "Close" not in df.columns:
            return "UNKNOWN"

        close = df["Close"]

        # Ensure it's a Series
        if not isinstance(close, pd.Series):
            return "UNKNOWN"

        if len(close) < 60:
            return "UNKNOWN"

        ma50 = close.rolling(50).mean()

        # Align and clean
        valid = pd.concat([close, ma50], axis=1)
        valid.columns = ["close", "ma50"]
        valid = valid.dropna()

        if valid.empty:
            return "UNKNOWN"

        last_close = valid["close"].iloc[-1]
        last_ma50 = valid["ma50"].iloc[-1]

        if last_close > last_ma50:
            return "BULL"
        else:
            return "BEAR"

    except Exception:
        return "UNKNOWN"
