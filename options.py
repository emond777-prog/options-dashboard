import numpy as np

def estimate_strike(price, option_type):
    if option_type == "PUT":
        # ~10% OTM
        return round(price * 0.90, 0)
    else:
        # ~10% OTM
        return round(price * 1.10, 0)


def estimate_probability(price, strike, option_type):
    distance = abs(price - strike) / price

    # crude mapping (can improve later)
    if distance >= 0.1:
        prob = 0.80
    elif distance >= 0.07:
        prob = 0.75
    elif distance >= 0.05:
        prob = 0.70
    else:
        prob = 0.60

    return prob


def estimate_premium(price, strike):
    # simple approximation (~1–2%)
    return round(price * 0.015, 2)


def estimate_return(premium, strike):
    return round((premium / strike) * 100, 2)
