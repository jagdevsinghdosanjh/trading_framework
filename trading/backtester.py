# trading/backtester.py
from dataclasses import dataclass
from typing import List, Dict, Any
import pandas as pd
from .indicators import atr


@dataclass
class BacktestConfig:
    initial_capital: float = 100000.0
    risk_per_trade: float = 0.01
    atr_window: int = 14
    atr_multiplier: float = 2.0
    commission_per_trade: float = 0.0
    sizing_mode: str = "atr"  # NEW: atr, vol, fixed_fraction, kelly_fraction
    vol_target: float = 0.02  # for vol sizing
    fixed_fraction: float = 0.5  # for fixed_fraction sizing
    kelly_fraction: float = 0.25  # for kelly sizing


def position_size_from_mode(equity, atr_value, price, config):
    """Unified sizing logic for all modes."""
    if config.sizing_mode == "atr":
        risk_amount = equity * config.risk_per_trade
        stop_distance = config.atr_multiplier * atr_value
        return risk_amount / stop_distance if stop_distance > 0 else 0

    if config.sizing_mode == "vol":
        return (equity * config.vol_target) / (price * 0.02)

    if config.sizing_mode == "fixed_fraction":
        return (equity * config.fixed_fraction) / price

    if config.sizing_mode == "kelly_fraction":
        return (equity * config.kelly_fraction) / price

    return 0


def apply_position_sizing(df: pd.DataFrame, config: BacktestConfig, teaching_mode=False):
    df = df.copy()
    df["atr"] = atr(df["high"], df["low"], df["close"], window=config.atr_window)
    df["position_dir"] = df["signal_final"].shift(1).fillna(0)

    equity = config.initial_capital
    shares_held = 0
    entry_price = 0.0

    equity_series = []
    position_series = []
    trade_equity_series = []
    exposure_series = []

    logs: List[Dict[str, Any]] = []

    for idx, row in df.iterrows():
        signal = row["position_dir"]
        price = row["close"]
        atr_value = row["atr"]

        # ENTRY
        if shares_held == 0 and signal != 0:
            shares = position_size_from_mode(equity, atr_value, price, config)
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

        # EXIT
        elif shares_held != 0 and (signal == 0 or (shares_held > 0 and signal < 0) or (shares_held < 0 and signal > 0)):
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

        # MARK-TO-MARKET
        equity_mt = equity + (shares_held * (price - entry_price) if shares_held != 0 else 0)

        equity_series.append(equity_mt)
        position_series.append(shares_held)
        exposure_series.append(1 if shares_held > 0 else -1 if shares_held < 0 else 0)

        # Trade equity only updates on exits
        trade_equity_series.append(equity if shares_held == 0 else None)

    df["position"] = position_series
    df["equity"] = equity_series
    df["returns"] = df["equity"].pct_change().fillna(0)
    df["exposure"] = exposure_series
    df["trade_equity"] = trade_equity_series

    # Drawdown
    df["peak_equity"] = df["equity"].cummax()
    df["drawdown"] = (df["equity"] - df["peak_equity"]) / df["peak_equity"]

    df.attrs["max_drawdown"] = float(df["drawdown"].min())
    df.attrs["max_drawdown_date"] = df["drawdown"].idxmin()

    return df, logs
