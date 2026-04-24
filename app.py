import streamlit as st
import pandas as pd

from engine import analyze_stock, generate_signal
from portfolio import load_positions
from pnl import compute_pnl
from rolling import rolling_decision
from market import market_trend

WATCHLIST = ["AAPL","MSFT","GOOGL","AMZN","AMD","TSLA"]

st.title("📊 Options Trading Dashboard")

# === MARKET ===
st.header("🌍 Market Regime")
st.write(market_trend())

# === SIGNALS ===
st.header("📡 Trade Signals")

signals = []

for ticker in WATCHLIST:
    data, close_series = analyze_stock(ticker)
    signal = generate_signal(ticker, data, close_series)

    if signal:
        signals.append({
            "Ticker": ticker,
            "Price": round(data["price"],2),
            "RSI": round(data["rsi"],1),
            "ADX": round(data["adx"],1),
            "Signal": signal
        })

st.dataframe(pd.DataFrame(signals))

# === PORTFOLIO ===
st.header("📁 Portfolio")

positions = load_positions()

if not positions.empty:
    pnl_df = compute_pnl(positions)
    pnl_df["Action"] = pnl_df.apply(rolling_decision, axis=1)

    st.dataframe(pnl_df)
else:
    st.write("No positions yet")