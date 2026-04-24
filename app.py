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

# Defaults
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
    st.sidebar.subheader("Manual Controls")
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
# MARKET REGIME
# =========================
st.header("🌍 Market Regime")
st.write(market_trend())


# =========================
# SCANNER
# =========================
@st.cache_data(ttl=3600)
def run_scan(params):
    return scan_market(get_universe(), params)

tickers = get_universe()
st.write(f"Scanning {len(tickers)} stocks")

results = scan_market(tickers, params)
results = run_scan(params)

st.header("📡 Best Trade Opportunities")


# =========================
# INTERACTIVE TABLE
# =========================
if results:
    df = pd.DataFrame(results)

    st.subheader("Click to add trade")

    # Header row
    h1, h2, h3, h4, h5, h6, h7 = st.columns(7)

    h1.markdown("**Ticker**")
    h2.markdown("**Signal**")
    h3.markdown("**Price**")
    h4.markdown("**Strike**")
    h5.markdown("**Premium**")
    h6.markdown("**Probability**")
    h7.markdown("**Action**")

    st.markdown("---")

    for i, row in df.iterrows():

        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

        col1.write(row["Ticker"])
        col2.write(row["Signal"])
        col3.markdown(f"**${row['Price']}**")
        col4.write(row["Strike"])
        col5.write(row["Premium"])
        col6.write(f"{row['Prob_%']}%")

        add_clicked = col7.button("Add", key=f"add_{i}")

        if add_clicked:
            st.session_state["selected_trade"] = row.to_dict()

    # =========================
    # CONFIRMATION PANEL
    # =========================
    if "selected_trade" in st.session_state:

        trade = st.session_state["selected_trade"]
        option_type = trade["Signal"].split()[1]

        st.markdown("---")
        st.subheader(f"📝 Confirm Trade: {trade['Ticker']}")

        col1, col2, col3 = st.columns(3)

        contracts = col1.number_input("Contracts", 1, 20, 1)
        from expiry import get_next_monthly_expiry
        default_expiry = get_next_monthly_expiry()
        expiry = col2.text_input("Expiry (YYYY-MM-DD)", default_expiry)
        premium = col3.number_input("Premium", value=float(trade["Premium"]))

        if st.button("✅ Confirm Add Trade"):

            new_trade = {
                "ticker": trade["Ticker"],
                "type": option_type,
                "strike": trade["Strike"],
                "expiry": expiry,
                "premium": premium,
                "contracts": contracts,
                "entry_price": trade["Price"],
                "current_price": None
            }

            save_position(new_trade)

            st.success(f"{trade['Ticker']} added to portfolio")

            del st.session_state["selected_trade"]

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
# PORTFOLIO
# =========================
st.header("📁 Portfolio")

positions = load_positions()

if not positions.empty:
    pnl_df = compute_pnl(positions)
    pnl_df["Action"] = pnl_df.apply(rolling_decision, axis=1)
    st.dataframe(pnl_df, use_container_width=True)
else:
    st.info("No positions yet")
