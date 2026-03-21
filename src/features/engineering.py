import pandas as pd

def add_basic_features(df: pd.DataFrame) -> pd.DataFrame:
    df['return'] = df['close'].pct_change()
    df['rolling_mean'] = df['close'].rolling(10).mean()
    df['rolling_std'] = df['close'].rolling(10).std()
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
    return df.dropna()
