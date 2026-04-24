import yfinance as yf
import pandas as pd

def market_trend():
    df = yf.download("SPY", period="6mo", interval="1d")

    if df.empty or len(df) < 60:
        return "UNKNOWN"

    close = df["Close"]
    ma50 = close.rolling(50).mean()

    # Drop NaN safely
    valid = pd.DataFrame({
        "close": close,
        "ma50": ma50
    }).dropna()

    if valid.empty:
        return "UNKNOWN"

    if valid["close"].iloc[-1] > valid["ma50"].iloc[-1]:
        return "BULL"
    else:
        return "BEAR"
