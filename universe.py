import pandas as pd

def get_universe():
    try:
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        tables = pd.read_html(url)
        sp500 = tables[0]

        tickers = sp500["Symbol"].tolist()
        tickers = [t.replace(".", "-") for t in tickers]

        return tickers

    except:
        return ["AAPL","MSFT","GOOGL","AMZN","META","NVDA","TSLA"]
