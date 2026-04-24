import streamlit as st
import pandas as pd

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

try:
    tickers = get_universe()
    results = scan_market(tickers)

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values(by="Score", ascending=False)

        st.dataframe(df, use_container_width=True)

    else:
        st.info("No high-quality setups right now")

except Exception:
    st.error("Scanner error - check logs")


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
