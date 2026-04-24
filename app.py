import streamlit as st
import pandas as pd
import yfinance as yf

from universe import get_universe
from scanner import scan_market

from portfolio import load_positions, save_position
from pnl import compute_pnl
from rolling import rolling_decision

from market import market_trend


st.set_page_config(page_title="Options Dashboard", layout="wide")
st.title("📊 Options Trading Dashboard")


# =========================
# SIDEBAR SETTINGS
# =========================
st.sidebar.header("⚙️ Strategy Settings")

mode = st.sidebar.selectbox(
    "Preset Mode",
    ["Conservative", "Balanced", "Aggressive", "Custom"]
)

rsi_low = 45
rsi_high = 60
adx_max = 35
bb_tol = 0.02

if mode == "Conservative":
    rsi_low = 35
    rsi_high = 65
    adx_max = 25
    bb_tol = 0.01

elif mode == "Balanced":
    rsi_low = 45
    rsi_high = 60
    adx_max = 35
    bb_tol = 0.02

elif mode == "Aggressive":
    rsi_low = 50
    rsi_high = 55
    adx_max = 45
    bb_tol = 0.04

if mode == "Custom":
    rsi_low = st.sidebar.slider("RSI Oversold", 20, 60, 45)
    rsi_high = st.sidebar.slider("RSI Overbought", 50, 80, 60)
    adx_max = st.sidebar.slider("Max ADX", 10, 50, 35)
    bb_tol = st.sidebar.slider("BB tolerance", 0.0, 0.05, 0.02)

params = {
    "rsi_low": rsi_low,
    "rsi_high": rsi_high,
    "adx_max": adx_max,
    "bb_tol": bb_tol
}

st.sidebar.json(params)


# =========================
# MARKET
# =========================
st.header("🌍 Market Regime")
st.write(market_trend())


# =========================
# SCANNER
# =========================
@st.cache_data(ttl=3600)
def run_scan(params):
    return scan_market(get_universe(), params)

results = run_scan(params)

st.header("📡 Best Trade Opportunities")

if results:
    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No setups today")


# =========================
# CHARTS
# =========================
st.header("📈 Top Charts")

for trade in results[:3]:
    ticker = trade["Ticker"]
    st.subheader(ticker)

    try:
        df_chart = yf.download(ticker, period="3mo")
        st.line_chart(df_chart["Close"])
    except:
        st.write("Chart error")


# =========================
# ADD TRADE
# =========================
st.header("➕ Add Trade")

with st.form("form"):
    ticker = st.text_input("Ticker")
    option_type = st.selectbox("Type", ["PUT","CALL"])
    strike = st.number_input("Strike", value=100.0)
    premium = st.number_input("Premium", value=1.0)
    contracts = st.number_input("Contracts", value=1)
    entry_price = st.number_input("Stock Price", value=100.0)
    expiry = st.text_input("Expiry", "2026-06-20")

    if st.form_submit_button("Add"):
        save_position({
            "ticker": ticker,
            "type": option_type,
            "strike": strike,
            "expiry": expiry,
            "premium": premium,
            "contracts": contracts,
            "entry_price": entry_price,
            "current_price": None
        })

        st.success("Trade added")


# =========================
# PORTFOLIO
# =========================
st.header("📁 Portfolio")

positions = load_positions()

if not positions.empty:
    pnl_df = compute_pnl(positions)
    pnl_df["Action"] = pnl_df.apply(rolling_decision, axis=1)
    st.dataframe(pnl_df)
else:
    st.info("No positions yet")
