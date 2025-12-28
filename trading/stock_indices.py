import pandas as pd
import numpy as np #noqa

def prepare_stock_indices(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Ensure datetime index
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame must have a DatetimeIndex before calling prepare_stock_indices.")

    # Use lowercase column names (your loader already normalizes them)
    close_col = "close"

    # Daily returns
    df["returns"] = df[close_col].pct_change()

    # Cumulative returns
    df["cum_returns"] = (1 + df["returns"]).cumprod()

    # Moving averages
    df["ma20"] = df[close_col].rolling(20).mean()
    df["ma50"] = df[close_col].rolling(50).mean()

    # Volatility (20-day rolling std)
    df["volatility20"] = df["returns"].rolling(20).std()

    # Rolling Sharpe ratio (20-day)
    df["sharpe20"] = (
        df["returns"].rolling(20).mean() /
        df["returns"].rolling(20).std()
    )

    return df
