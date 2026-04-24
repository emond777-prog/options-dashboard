import pandas as pd

def compute_pnl(df):
    results = []

    for _, row in df.iterrows():
        if pd.isna(row["current_price"]):
            continue

        pnl = (row["premium"] - row["current_price"]) * 100 * row["contracts"]
        pct = (row["premium"] - row["current_price"]) / row["premium"]

        results.append({
            "ticker": row["ticker"],
            "type": row["type"],
            "PnL_$": round(pnl,2),
            "PnL_%": round(pct*100,1)
        })

    return pd.DataFrame(results)