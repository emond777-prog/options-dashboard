import yfinance as yf
import pandas as pd

from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from ta.trend import ADXIndicator


def analyze_stock(ticker):
    try:
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

        aligned = pd.concat([high, low, close], axis=1)
        aligned.columns = ["high", "low", "close"]
        aligned = aligned.dropna()

        if len(aligned) < 50:
            return None, None

        high = aligned["high"]
        low = aligned["low"]
        close = aligned["close"]

        bb = BollingerBands(close, 20, 2)
        rsi = RSIIndicator(close, 14).rsi()
        adx = ADXIndicator(high, low, close, 14).adx()

        data = {
            "price": close.iloc[-1],
            "bb_high": bb.bollinger_hband().iloc[-1],
            "bb_low": bb.bollinger_lband().iloc[-1],
            "rsi": rsi.iloc[-1],
            "adx": adx.iloc[-1],
        }

        return data, close

    except:
        return None, None


def generate_signal(ticker, d, close_series, params):
    if d is None:
        return None

    try:
        rsi_low = params["rsi_low"]
        rsi_high = params["rsi_high"]
        adx_max = params["adx_max"]
        bb_tol = params["bb_tol"]

        if (
            d["price"] < d["bb_low"] * (1 + bb_tol)
            and d["rsi"] < rsi_low
            and d["adx"] < adx_max
        ):
            return "SELL PUT"

        if (
            d["price"] > d["bb_high"] * (1 - bb_tol)
            and d["rsi"] > rsi_high
            and d["adx"] < adx_max
        ):
            return "SELL CALL"

        return None

    except:
        return None
