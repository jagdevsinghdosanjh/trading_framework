# trading/backtester.py
from dataclasses import dataclass
from typing import Optional #noqa

import pandas as pd

from .indicators import atr


@dataclass
class BacktestConfig:
    initial_capital: float = 100000.0
    risk_per_trade: float = 0.01   # fraction of equity (e.g. 0.01 = 1%)
    atr_window: int = 14
    atr_multiplier: float = 2.0
    commission_per_trade: float = 0.0

def apply_position_sizing(
    df: pd.DataFrame,
    config: BacktestConfig,
    teaching_mode: bool = False,
):
    df = df.copy()
    df["atr"] = atr(df["high"], df["low"], df["close"], window=config.atr_window)
    df["position_dir"] = df["signal_final"].shift(1).fillna(0)

    equity = config.initial_capital
    position_size = []
    equity_series = []

    shares_held = 0
    entry_price = 0.0

    logs = []  # <--- ADD THIS

    for idx, row in df.iterrows():
        signal = row["position_dir"]
        price = row["close"]
        current_atr = row["atr"]

        if shares_held == 0:
            if signal != 0 and pd.notna(current_atr) and current_atr > 0:
                risk_amount = equity * config.risk_per_trade
                stop_distance = config.atr_multiplier * current_atr
                if stop_distance > 0:
                    shares = risk_amount / stop_distance
                    shares_held = signal * shares
                    entry_price = price

                    if teaching_mode:
                        logs.append({
                            "timestamp": idx,
                            "action": "ENTRY",
                            "signal": signal,
                            "shares": shares_held,
                            "price": price,
                            "equity": equity,
                        })

        else:
            if signal == 0 or (shares_held > 0 and signal < 0) or (shares_held < 0 and signal > 0):
                pnl = shares_held * (price - entry_price)
                equity += pnl - config.commission_per_trade

                if teaching_mode:
                    logs.append({
                        "timestamp": idx,
                        "action": "EXIT",
                        "signal": signal,
                        "shares": shares_held,
                        "price": price,
                        "pnl": pnl,
                        "equity": equity,
                    })

                shares_held = 0
                entry_price = 0.0

        equity_mt = equity
        if shares_held != 0:
            equity_mt += shares_held * (price - entry_price)

        equity_series.append(equity_mt)
        position_size.append(shares_held)

    df["position"] = position_size
    df["equity"] = equity_series
    df["returns"] = df["equity"].pct_change().fillna(0.0)

    return df, logs  # <--- FIXED


# def apply_position_sizing(
#     df: pd.DataFrame,
#     config: BacktestConfig,
#     teaching_mode: bool = False,
# ) -> pd.DataFrame:
#     """
#     Uses ATR-based stop to size positions.
#     """
#     df = df.copy()
#     df["atr"] = atr(df["high"], df["low"], df["close"], window=config.atr_window)

#     # Position entered based on signal from previous bar
#     df["position_dir"] = df["signal_final"].shift(1).fillna(0)

#     equity = config.initial_capital
#     position_size = []
#     equity_series = []

#     shares_held = 0
#     entry_price = 0.0

#     for idx, row in df.iterrows():
#         signal = row["position_dir"]
#         price = row["close"]
#         current_atr = row["atr"]

#         if shares_held == 0:
#             # No open position; look for new entry
#             if signal != 0 and pd.notna(current_atr) and current_atr > 0:
#                 risk_amount = equity * config.risk_per_trade
#                 stop_distance = config.atr_multiplier * current_atr
#                 if stop_distance > 0:
#                     shares = risk_amount / stop_distance
#                     shares_held = signal * shares
#                     entry_price = price
#         else:
#             # Exit if signal goes flat or reverses
#             if signal == 0 or (shares_held > 0 and signal < 0) or (shares_held < 0 and signal > 0):
#                 equity += shares_held * (price - entry_price) - config.commission_per_trade
#                 shares_held = 0
#                 entry_price = 0.0

#         # Mark-to-market equity
#         equity_mt = equity
#         if shares_held != 0:
#             equity_mt += shares_held * (price - entry_price)

#         equity_series.append(equity_mt)
#         position_size.append(shares_held)

#     df["position"] = position_size
#     df["equity"] = equity_series
#     df["returns"] = df["equity"].pct_change().fillna(0.0)

#     return df
