from engine import analyze_stock, generate_signal
from options import (
    estimate_strike,
    estimate_probability,
    estimate_premium,
    estimate_return
)

def score_trade(data):
    score = 0

    if data["rsi"] < 30 or data["rsi"] > 70:
        score += 2

    if data["adx"] < 25:
        score += 1

    return score


def scan_market(tickers, params):
    results = []

    for ticker in tickers:
        try:
            data, close = analyze_stock(ticker)

            if data is None:
                continue

            signal = generate_signal(ticker, data, close, params)

            if signal:
                option_type = signal.split()[1]

                strike = estimate_strike(data["price"], option_type)
                prob = estimate_probability(data["price"], strike, option_type)
                premium = estimate_premium(data["price"], strike)
                ret = estimate_return(premium, strike)

                score = score_trade(data)

                results.append({
                    "Ticker": ticker,
                    "Signal": signal,
                    "Price": round(data["price"], 2),
                    "Strike": strike,
                    "Premium": premium,
                    "Return_%": ret,
                    "Prob_%": round(prob * 100, 1),
                    "Score": score
                })

        except:
            continue

    results = sorted(results, key=lambda x: x["Score"], reverse=True)

    return results[:10]
