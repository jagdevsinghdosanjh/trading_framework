import matplotlib.pyplot as plt
import pandas as pd

def plot_equity_curve(df: pd.DataFrame, title: str = "Equity Curve") -> None:
    plt.figure(figsize=(10, 5))
    df["equity"].plot()
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_drawdown(df: pd.DataFrame, title: str = "Drawdown") -> None:
    equity = df["equity"]
    roll_max = equity.cummax()
    dd = equity / roll_max - 1.0

    plt.figure(figsize=(10, 4))
    dd.plot(color="red")
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
