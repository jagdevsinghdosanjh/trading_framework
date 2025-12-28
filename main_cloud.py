from fastapi import FastAPI
from pydantic import BaseModel

from trading.data_loader import load_csv, resample_ohlcv
from trading.strategies import hybrid_swing_strategy
from trading.backtester import BacktestConfig, apply_position_sizing
from trading.metrics import sharpe_ratio, max_drawdown, cagr

app = FastAPI()

class BacktestRequest(BaseModel):
    data_path: str
    timeframe: str = "D"
    initial_capital: float = 100000
    risk_per_trade: float = 0.01
    atr_window: int = 14
    atr_multiplier: float = 2.0
    commission_per_trade: float = 0.0

@app.post("/backtest/hybrid_swing")
def backtest_hybrid(req: BacktestRequest):
    df = load_csv(req.data_path)
    if req.timeframe:
        df = resample_ohlcv(df, req.timeframe)

    df = hybrid_swing_strategy(df)

    cfg = BacktestConfig(
        initial_capital=req.initial_capital,
        risk_per_trade=req.risk_per_trade,
        atr_window=req.atr_window,
        atr_multiplier=req.atr_multiplier,
        commission_per_trade=req.commission_per_trade,
    )

    bt_df, _ = apply_position_sizing(df, cfg, teaching_mode=False)

    return {
        "final_equity": float(bt_df["equity"].iloc[-1]),
        "sharpe_ratio": float(sharpe_ratio(bt_df["returns"])),
        "max_drawdown": float(max_drawdown(bt_df["equity"])),
        "cagr": float(cagr(bt_df["equity"])),
    }
