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
from trading.report_generator import generate_pdf_report
from trading.stock_indices import prepare_stock_indices
from trading.stock_plots import (
    plot_equity_curve as plot_stock_equity_curve,
    plot_cumulative_returns,
    plot_moving_averages,
    plot_volatility,
    plot_sharpe,
)

# Collect all PNGs from current folder
png_files = sorted([
    str(p) for p in Path(".").glob("*.png")
    if p.is_file() and p.suffix == ".png"
])

# Generate PDF report
generate_pdf_report(png_files)


def select_csv_cli(data_folder: Path) -> str:
    """CLI selector for CSV files inside the data folder."""
    csv_files = sorted([f.name for f in data_folder.glob("*.csv")])

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {data_folder}")

    print("\n📁 Available CSV files:")
    for i, file in enumerate(csv_files, start=1):
        print(f"{i}. {file}")

    while True:
        try:
            choice = int(input(f"\nSelect a file (1-{len(csv_files)}): "))
            if 1 <= choice <= len(csv_files):
                return csv_files[choice - 1]
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")


def main() -> None:
    # Load config
    base_dir = Path(__file__).resolve().parent
    cfg_path = base_dir / "config" / "local_config.yaml"
    cfg: Dict[str, Any] = load_yaml(str(cfg_path))

    # Data folder
    data_folder = base_dir / cfg["data_folder"]

    # CLI selection (fallback if YAML has null)
    selected_csv = cfg.get("selected_csv")
    if not selected_csv:
        selected_csv = select_csv_cli(data_folder)

    data_file = data_folder / selected_csv
    print(f"\n📄 Loading CSV: {selected_csv}")

    # Load CSV
    df: pd.DataFrame = load_csv(str(data_file))

    # Optional resampling
    if cfg.get("timeframe"):
        df = resample_ohlcv(df, cfg["timeframe"])

    # Stock indices
    df = prepare_stock_indices(df)

    # Strategy
    df = hybrid_swing_strategy(df)

    # Backtest config
    bt_cfg = BacktestConfig(
        initial_capital=cfg["initial_capital"],
        risk_per_trade=cfg["risk_per_trade"],
        atr_window=cfg["atr_window"],
        atr_multiplier=cfg["atr_multiplier"],
        commission_per_trade=cfg["commission_per_trade"],
    )

    # Run backtest
    bt_df, logs = cast(
        Tuple[pd.DataFrame, List[Dict[str, Any]]],
        apply_position_sizing(df, bt_cfg, teaching_mode=True),
    )

    # Metrics
    print("\n📊 Backtest Results")
    print("Final equity:", float(bt_df["equity"].iloc[-1]))
    print("Sharpe ratio:", float(sharpe_ratio(bt_df["returns"])))
    print("Max drawdown:", float(max_drawdown(bt_df["equity"])))
    print("CAGR:", float(cagr(bt_df["equity"])))

    # Teaching log
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
