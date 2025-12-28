# trading/stock_indices.py

import pandas as pd
import numpy as np #noqa

def prepare_stock_indices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds key stock indices to the DataFrame:
    - Daily returns
    - Cumulative returns
    - 20-day and 50-day moving averages
    - Rolling volatility (20-day std)
    - Rolling Sharpe ratio (20-day)
    """

    df = df.copy()

    # Ensure datetime index
    if not isinstance(df.index, pd.DatetimeIndex):
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date")
        else:
            raise ValueError("DataFrame must contain a 'date' column or DatetimeIndex")

    # Daily returns
    df["returns"] = df["Close"].pct_change()

    # Cumulative returns
    df["cum_returns"] = (1 + df["returns"]).cumprod()

    # Moving averages
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()

    # Volatility (20-day rolling std)
    df["volatility20"] = df["returns"].rolling(20).std()

    # Rolling Sharpe ratio (20-day)
    df["sharpe20"] = (
        df["returns"].rolling(20).mean() /
        df["returns"].rolling(20).std()
    )

    return df
