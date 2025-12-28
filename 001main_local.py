from pathlib import Path
from typing import Dict, Any, Tuple, List, cast
import pandas as pd

from trading.utils import load_yaml
from trading.data_loader import load_csv, resample_ohlcv
from trading.strategies import hybrid_swing_strategy
from trading.backtester import BacktestConfig, apply_position_sizing
from trading.metrics import sharpe_ratio, max_drawdown, cagr
from trading.plotting import plot_equity_curve as plot_bt_equity_curve, plot_drawdown
from trading.teaching import print_teaching_log

from trading.stock_indices import prepare_stock_indices
from trading.stock_plots import (
    plot_equity_curve as plot_stock_equity_curve,
    plot_cumulative_returns,
    plot_moving_averages,
    plot_volatility,
    plot_sharpe,
)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    cfg_path = base_dir / "config" / "local_config.yaml"

    cfg: Dict[str, Any] = load_yaml(str(cfg_path))

    df: pd.DataFrame = load_csv(cfg["data_path"])
    if cfg.get("timeframe"):
        df = resample_ohlcv(df, cfg["timeframe"])

    # Stock indices (analytics)
    df = prepare_stock_indices(df)

    # Apply strategy
    df = hybrid_swing_strategy(df)

    # Backtest config
    bt_cfg = BacktestConfig(
        initial_capital=cfg["initial_capital"],
        risk_per_trade=cfg["risk_per_trade"],
        atr_window=cfg["atr_window"],
        atr_multiplier=cfg["atr_multiplier"],
        commission_per_trade=cfg["commission_per_trade"],
    )

    bt_df, logs = cast(
        Tuple[pd.DataFrame, List[Dict[str, Any]]],
        apply_position_sizing(df, bt_cfg, teaching_mode=True),
    )

    print("Final equity:", float(bt_df["equity"].iloc[-1]))
    print("Sharpe ratio:", float(sharpe_ratio(bt_df["returns"])))
    print("Max drawdown:", float(max_drawdown(bt_df["equity"])))
    print("CAGR:", float(cagr(bt_df["equity"])))

    print("\n--- Teaching log (first trades) ---")
    print_teaching_log(logs, max_rows=20)

    # Backtest plots
    plot_bt_equity_curve(bt_df, title="Equity Curve - Hybrid Swing")
    plot_drawdown(bt_df, title="Drawdown - Hybrid Swing")

    # Stock analytics plots
    plot_stock_equity_curve(df)
    plot_cumulative_returns(df)
    plot_moving_averages(df)
    plot_volatility(df)
    plot_sharpe(df)


if __name__ == "__main__":
    main()
