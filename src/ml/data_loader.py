import pandas as pd

def load_ohlcv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=['timestamp'])
    df = df.sort_values('timestamp')
    df = df.set_index('timestamp')
    return df
