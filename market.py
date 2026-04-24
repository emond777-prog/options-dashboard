import yfinance as yf

def market_trend():
    df = yf.download("SPY", period="6mo", interval="1d")

    close = df["Close"]
    ma50 = close.rolling(50).mean()

    if close.iloc[-1] > ma50.iloc[-1]:
        return "BULL"
    else:
        return "BEAR"
