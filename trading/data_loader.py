import os
import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    """Load CSV and normalize timestamp/date + OHLC columns."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")

    df = pd.read_csv(path)

    # Normalize column names to lowercase
    df.columns = [c.lower() for c in df.columns]

    # Accept both 'timestamp' and 'date'
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    elif "date" in df.columns:
        df["timestamp"] = pd.to_datetime(df["date"])
    else:
        raise KeyError("CSV must contain either 'timestamp' or 'date' column.")

    # Set timestamp as index
    df = df.set_index("timestamp")

    # Normalize OHLC column names (open, high, low, close, volume)
    rename_map = {
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
        "v": "volume",
        "o": "open",
        "h": "high",
        "l": "low",
        "c": "close",
    }

    df = df.rename(columns=rename_map)

    # Ensure required OHLC columns exist
    required_cols = ["open", "high", "low", "close"]
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"CSV missing required column: '{col}'")

    # Sort index (important for resampling + strategy)
    df = df.sort_index()

    return df


def resample_ohlcv(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    """Resample OHLCV data to a new timeframe."""
    def ohlcv(group: pd.DataFrame) -> pd.Series:
        return pd.Series({
            "open": group["open"].iloc[0],
            "high": group["high"].max(),
            "low": group["low"].min(),
            "close": group["close"].iloc[-1],
            "volume": group["volume"].sum(),
        })

    return df.resample(rule).apply(ohlcv).dropna()
