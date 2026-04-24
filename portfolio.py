import pandas as pd

FILE = "positions.csv"

def load_positions():
    try:
        return pd.read_csv(FILE)
    except:
        return pd.DataFrame(columns=[
            "ticker","type","strike","expiry",
            "premium","contracts","entry_price","current_price"
        ])


def save_position(new_row):
    df = load_positions()
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FILE, index=False)
