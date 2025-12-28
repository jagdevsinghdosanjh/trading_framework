# trading/metrics.py
import numpy as np
import pandas as pd


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Annualized Sharpe ratio.
    """
    if returns.std() == 0:
        return 0.0

    excess = returns - risk_free_rate / periods_per_year
    return float(np.sqrt(periods_per_year) * excess.mean() / excess.std())


def max_drawdown(equity_curve: pd.Series) -> float:
    """
    Maximum drawdown as a negative fraction.
    """
    roll_max = equity_curve.cummax()
    drawdown = equity_curve / roll_max - 1.0
    return float(drawdown.min())


def cagr(
    equity_curve: pd.Series,
    periods_per_year: int = 252,
) -> float:
    """
    Compound annual growth rate.
    """
    if len(equity_curve) < 2:
        return 0.0

    total_return = equity_curve.iloc[-1] / equity_curve.iloc[0]
    years = len(equity_curve) / periods_per_year
    if years <= 0:
        return 0.0
    return float(total_return ** (1 / years) - 1)
