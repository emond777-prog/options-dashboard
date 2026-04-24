def rolling_decision(row):
    if row["PnL_%"] >= 60:
        return "CLOSE"

    if row["type"] == "CALL" and row["PnL_%"] < 0:
        return "ROLL UP"

    if row["type"] == "PUT" and row["PnL_%"] < 0:
        return "ROLL DOWN"

    return "HOLD"