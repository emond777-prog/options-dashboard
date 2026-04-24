import streamlit as st
import pandas as pd
import yfinance as yf

from universe import get_universe
from scanner import scan_market

from portfolio import load_positions, save_position
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
# SCANNER (CACHED)
# =========================
@st.cache_data(ttl=3600)
def run_scan():
    tickers = get_universe()
    return scan_market(tickers)


st.header("📡 Best Trade Opportunities")

results = []

try:
    results = run_scan()

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values(by="Score", ascending=False)

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

except Exception:
    st.error("Scanner error - check logs")


# =========================
# CHARTS (TOP TRADES)
# =========================
st.header("📈 Top Charts")

if results:
    top = results[:3]

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
# ADD TRADE (AUTO CSV)
# =========================
st.header("➕ Add Trade")

with st.form("add_trade_form"):

    col1, col2 = st.columns(2)

    ticker = col1.text_input("Ticker", value="AAPL")
    option_type = col2.selectbox("Type", ["PUT", "CALL"])

    col3, col4 = st.columns(2)

    strike = col3.number_input("Strike", value=100.0)
    premium = col4.number_input("Premium", value=1.0)

    col5, col6 = st.columns(2)

    contracts = col5.number_input("Contracts", value=1)
    entry_price = col6.number_input("Stock Price", value=100.0)

    expiry = st.text_input("Expiry (YYYY-MM-DD)", value="2026-06-20")

    submitted = st.form_submit_button("Add Position")

    if submitted:
        new_trade = {
            "ticker": ticker,
            "type": option_type,
            "strike": strike,
            "expiry": expiry,
            "premium": premium,
            "contracts": contracts,
            "entry_price": entry_price,
            "current_price": None
        }

        save_position(new_trade)

        st.success(f"Trade added: {ticker}")


# =========================
# PORTFOLIO
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
