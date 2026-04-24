import numpy as np

def compute_iv_rank(close):
    returns = close.pct_change().dropna()
    vol = returns.rolling(20).std() * np.sqrt(252)

    current = vol.iloc[-1]
    min_v = vol.min()
    max_v = vol.max()

    if max_v == min_v:
        return 0

    return (current - min_v) / (max_v - min_v)