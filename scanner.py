from engine import analyze_stock, generate_signal

def score_trade(data):
    score = 0

    # stronger extremes = higher score
    if data["rsi"] < 30 or data["rsi"] > 70:
        score += 2

    if abs(data["price"] - data["bb_low"]) < 1 or abs(data["price"] - data["bb_high"]) < 1:
        score += 2

    if data["adx"] < 20:
        score += 1

    return score


def scan_market(tickers):
    results = []

    for ticker in tickers:
        try:
            data, close = analyze_stock(ticker)

            if data is None:
                continue

            signal = generate_signal(ticker, data, close)

            if signal:
                score = score_trade(data)

                results.append({
                    "Ticker": ticker,
                    "Signal": signal,
                    "Price": round(data["price"],2),
                    "RSI": round(data["rsi"],1),
                    "Score": score
                })

        except:
            continue

    # Sort best first
    results = sorted(results, key=lambda x: x["Score"], reverse=True)

    return results[:10]  # top 10 trades
