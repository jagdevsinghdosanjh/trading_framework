import pandas as pd
from .indicators import ema, rsi

def add_trend_filter(df: pd.DataFrame, slow_window: int = 50, fast_window: int = 20) -> pd.DataFrame:
    df = df.copy()
    df["slow_trend"] = ema(df["close"], slow_window)
    df["fast_trend"] = ema(df["close"], fast_window)

    df["trend"] = 0
    df.loc[df["fast_trend"] > df["slow_trend"], "trend"] = 1
    df.loc[df["fast_trend"] < df["slow_trend"], "trend"] = -1

    return df

def trend_pullback_strategy(
    df: pd.DataFrame,
    ema_window: int = 20,
    rsi_window: int = 14,
    rsi_buy: int = 40,
    rsi_sell: int = 60,
) -> pd.DataFrame:
    df = df.copy()
    df["ema"] = ema(df["close"], ema_window)
    df["rsi"] = rsi(df["close"], rsi_window)
    df["signal"] = 0

    long_cond = (df["trend"] == 1) & (df["close"] <= df["ema"]) & (df["rsi"] < rsi_buy)
    short_cond = (df["trend"] == -1) & (df["close"] >= df["ema"]) & (df["rsi"] > rsi_sell)

    df.loc[long_cond, "signal"] = 1
    df.loc[short_cond, "signal"] = -1

    return df

def mean_reversion_strategy(
    df: pd.DataFrame,
    rsi_window: int = 14,
    low: int = 30,
    high: int = 70,
) -> pd.DataFrame:
    df = df.copy()
    df["rsi"] = rsi(df["close"], rsi_window)
    df["signal"] = 0

    df.loc[df["rsi"] < low, "signal"] = 1
    df.loc[df["rsi"] > high, "signal"] = -1

    return df

def hybrid_swing_strategy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Simple moving average crossover strategy
    df["sma_fast"] = df["close"].rolling(window=3).mean()
    df["sma_slow"] = df["close"].rolling(window=5).mean()

    # Generate signal: +1 for long, -1 for short, 0 for flat
    df["signal_raw"] = 0
    df.loc[df["sma_fast"] > df["sma_slow"], "signal_raw"] = 1
    df.loc[df["sma_fast"] < df["sma_slow"], "signal_raw"] = -1

    # Final signal with smoothing (optional)
    df["signal_final"] = df["signal_raw"].rolling(window=2).mean().round().fillna(0)

    return df