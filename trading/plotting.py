import matplotlib.pyplot as plt


def plot_equity_curve(df, title="Equity Curve - Hybrid Swing"):
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df["equity"], label="Equity")
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.grid(True)
    plt.legend()
    plt.savefig("equity_curve_hybrid_swing.png", bbox_inches="tight")
    plt.close()


def plot_drawdown(df, title="Drawdown - Hybrid Swing"):
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df["drawdown"], color="red")
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.savefig("drawdown_hybrid_swing.png", bbox_inches="tight")
    plt.close()
