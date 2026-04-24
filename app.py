import streamlit as st
import pandas as pd
import yfinance as yf

from universe import get_universe
from scanner import scan_market

from portfolio import load_positions
from pnl import compute_pnl
from rolling import rolling_decision

from market import market_trend


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Options Dashboard", layout="wide")

st.title("📊 Options Trading Dashboard")


# =========================
# MARKET REGIME
# =========================
st.header("🌍 Market Regime")

try:
    regime = market_trend()
except:
    regime = "UNKNOWN"

st.write(regime)


# =========================
# TRADE SCANNER
# =========================
st.header("📡 Best Trade Opportunities")

results = []

try:
    tickers = get_universe()
    results = scan_market(tickers)

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values(by="Score", ascending=False)

        # Color signals
        def color_signal(val):
            if val == "SELL PUT":
                return "color: green"
            elif val == "SELL CALL":
                return "color: red"
            return ""

        st.dataframe(
            df.style.applymap(color_signal, subset=["Signal"]),
            use_container_width=True
        )

    else:
        st.info("No high-quality setups right now")

except Exception as e:
    st.error("Scanner error - check logs")


# =========================
# CHARTS SECTION
# =========================
st.header("📈 Top Charts")

if results:
    top = results[:3]  # show top 3 opportunities

    for trade in top:
        ticker = trade["Ticker"]
        signal = trade["Signal"]

        st.subheader(f"{ticker} → {signal}")

        try:
            df_chart = yf.download(ticker, period="3mo", interval="1d")

            if df_chart is not None and not df_chart.empty:
                st.line_chart(df_chart["Close"])
            else:
                st.write("No chart data")

        except:
            st.write("Chart error")


# =========================
# PORTFOLIO SECTION
# =========================
st.header("📁 Portfolio")

positions = load_positions()

if positions is not None and not positions.empty:

    try:
        pnl_df = compute_pnl(positions)

        if pnl_df is not None and not pnl_df.empty:
            pnl_df["Action"] = pnl_df.apply(rolling_decision, axis=1)

            st.dataframe(pnl_df, use_container_width=True)
        else:
            st.info("No active PnL data yet")

    except Exception:
        st.error("Error computing portfolio")

else:
    st.info("No positions yet")
