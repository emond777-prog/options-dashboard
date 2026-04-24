def generate_signal(ticker, d, close_series, params):
    if d is None:
        return None

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
