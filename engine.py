import yfinance as yf
import pandas as pd

from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from ta.trend import ADXIndicator

from volatility import compute_iv_rank
from market import market_trend


def analyze_stock(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")

    if df is None or df.empty:
        return None, None

    if not all(col in df.columns for col in ["Close", "High", "Low"]):
        return None, None

    close = df["Close"]
    high = df["High"]
    low = df["Low"]

    # Ensure 1D
    if hasattr(close, "ndim") and close.ndim > 1:
        close = close.squeeze()
    if hasattr(high, "ndim") and high.ndim > 1:
        high = high.squeeze()
    if hasattr(low, "ndim") and low.ndim > 1:
        low = low.squeeze()

    # Align all series
    aligned = pd.concat([high, low, close], axis=1)
    aligned.columns = ["high", "low", "close"]
    aligned = aligned.dropna()

    if len(aligned) < 50:
        return None, None

    high = aligned["high"]
    low = aligned["low"]
    close = aligned["close"]

    # Indicators
    bb = BollingerBands(close, 20, 2)
    rsi = RSIIndicator(close, 14).rsi()
    adx = ADXIndicator(high, low, close, 14).adx()
    ma200 = close.rolling(200).mean()

    data = {
        "price": close.iloc[-1],
        "bb_high": bb.bollinger_hband().iloc[-1],
        "bb_low": bb.bollinger_lband().iloc[-1],
        "rsi": rsi.iloc[-1],
        "adx": adx.iloc[-1],
        "ma200": ma200.iloc[-1]
    }

    return data, close


def generate_signal(ticker, d, close_series):
    if d is None:
        return None

    iv_rank = compute_iv_rank(close_series)
    regime = market_trend()

    if (
        d["price"] < d["bb_low"]
        and d["price"] > d["ma200"]
        and d["rsi"] < 35
        and d["adx"] < 25
        and iv_rank > 0.5
        and regime == "BULL"
    ):
        return "SELL PUT"

    if (
        d["price"] > d["bb_high"]
        and d["rsi"] > 65
        and d["adx"] < 30
        and iv_rank > 0.4
    ):
        return "SELL CALL"

    return None
