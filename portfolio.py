import pandas as pd

FILE = "positions.csv"

def load_positions():
    try:
        return pd.read_csv(FILE)
    except:
        return pd.DataFrame()