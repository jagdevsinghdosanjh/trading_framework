from pathlib import Path
from typing import Dict, Any, Tuple, List, cast
import pandas as pd

from trading.utils import load_yaml
from trading.data_loader import load_csv, resample_ohlcv
from trading.strategies import hybrid_swing_strategy
from trading.backtester import BacktestConfig, apply_position_sizing
from trading.metrics import sharpe_ratio, max_drawdown, cagr
from trading.plotting import plot_equity_curve, plot_drawdown
from trading.teaching import print_teaching_log


def main() -> None:
    # Resolve config path relative to this file
    base_dir = Path(__file__).resolve().parent
    cfg_path = base_dir / "config" / "local_config.yaml"

    # Load configuration
    cfg: Dict[str, Any] = load_yaml(str((cfg_path)))

    # Load and optionally resample data
    df: pd.DataFrame = load_csv(cfg["data_path"])
    if cfg.get("timeframe"):
        df = resample_ohlcv(df, cfg["timeframe"])

    # Apply strategy
    df = hybrid_swing_strategy(df)

    # Backtest configuration
    bt_cfg = BacktestConfig(
        initial_capital=cfg["initial_capital"],
        risk_per_trade=cfg["risk_per_trade"],
        atr_window=cfg["atr_window"],
        atr_multiplier=cfg["atr_multiplier"],
        commission_per_trade=cfg["commission_per_trade"],
    )

    # Run backtest (must return DataFrame + logs)
    bt_df, logs = cast(
        Tuple[pd.DataFrame, List[Dict[str, Any]]],
        apply_position_sizing(df, bt_cfg, teaching_mode=True),
    )

    # Print metrics
    print("Final equity:", float(bt_df["equity"].iloc[-1]))
    print("Sharpe ratio:", float(sharpe_ratio(bt_df["returns"])))
    print("Max drawdown:", float(max_drawdown(bt_df["equity"])))
    print("CAGR:", float(cagr(bt_df["equity"])))

    # Teaching log
    print("\n--- Teaching log (first trades) ---")
    print_teaching_log(logs, max_rows=20)

    # Plots
    plot_equity_curve(bt_df, title="Equity Curve - Hybrid Swing")
    plot_drawdown(bt_df, title="Drawdown - Hybrid Swing")


if __name__ == "__main__":
    main()
