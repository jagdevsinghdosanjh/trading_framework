from pathlib import Path #noqa
import pandas as pd
from trading.data_loader import load_csv
from trading.stock_indices import prepare_stock_indices
from trading.strategies import hybrid_swing_strategy
from trading.backtester import apply_position_sizing, BacktestConfig


def run_portfolio_backtest(csv_files, config: BacktestConfig):
    results = {}
    for file in csv_files:
        df = load_csv(file)
        df = prepare_stock_indices(df)
        df = hybrid_swing_strategy(df)
        bt_df, logs = apply_position_sizing(df, config)
        results[file] = bt_df

    # Align all equities by date
    combined = pd.concat(
        {k: v["equity"] for k, v in results.items()},
        axis=1
    ).fillna(method="ffill")

    combined["portfolio_equity"] = combined.mean(axis=1)
    combined["portfolio_returns"] = combined["portfolio_equity"].pct_change()

    return combined, results
