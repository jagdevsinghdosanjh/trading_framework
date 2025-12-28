import os #noqa
import pandas as pd
# def load_csv(path: str, parse_dates: bool = True, date_col: str = "date") -> pd.DataFrame:
#     if not os.path.exists(path):
#         raise FileNotFoundError(f"Data file not found: {path}")

#     df = pd.read_csv(path)

#     if parse_dates and date_col in df.columns:
#         df[date_col] = pd.to_datetime(df[date_col])
#         df = df.set_index(date_col).sort_index()

#     return df

def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Ensure timestamp column exists
    # Normalize column names
df.columns = [c.lower() for c in df.columns]

# Accept both 'timestamp' and 'date'
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
elif "date" in df.columns:
    df["timestamp"] = pd.to_datetime(df["date"])
else:
    raise KeyError("CSV must contain either 'timestamp' or 'date' column.")

# Set index
df = df.set_index("timestamp")


    # if "timestamp" not in df.columns:
    #     raise KeyError("CSV must contain a 'timestamp' column.")

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")

    # Set timestamp as index
    df = df.set_index("timestamp")

    # Sort index (important for resampling)
    df = df.sort_index()

    return df


# def resample_ohlcv(df: pd.DataFrame, rule: str = "D") -> pd.DataFrame:
#     ohlc = {
#         "open": "first",
#         "high": "max",
#         "low": "min",
#         "close": "last",
#         "volume": "sum",
#     }
#     return df.resample(rule).agg(ohlc).dropna()
# def resample_ohlcv(df: pd.DataFrame, rule: str) -> pd.DataFrame:
#     agg_map = {
#         "open": ["first"],
#         "high": ["max"],
#         "low": ["min"],
#         "close": ["last"],
#         "volume": ["sum"],
#     }

#     resampled = df.resample(rule).agg(agg_map)

#     # Flatten MultiIndex columns: ('open', 'first') → 'open'
#     resampled.columns = [col[0] for col in resampled.columns]

#     return resampled.dropna()
def resample_ohlcv(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    def ohlcv(group: pd.DataFrame) -> pd.Series:
        return pd.Series({
            "open": group["open"].iloc[0],
            "high": group["high"].max(),
            "low": group["low"].min(),
            "close": group["close"].iloc[-1],
            "volume": group["volume"].sum(),
        })

    return df.resample(rule).apply(ohlcv).dropna()
