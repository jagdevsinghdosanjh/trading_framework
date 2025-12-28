import matplotlib.pyplot as plt


def plot_equity_curve(df):
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df["close"], label="Close Price")
    plt.title("Equity Curve")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend()
    plt.savefig("stock_equity_curve.png", bbox_inches="tight")
    plt.close()


def plot_cumulative_returns(df):
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df["cum_returns"], label="Cumulative Returns", color="purple")
    plt.title("Cumulative Returns")
    plt.xlabel("Time")
    plt.ylabel("Growth")
    plt.grid(True)
    plt.legend()
    plt.savefig("cumulative_returns.png", bbox_inches="tight")
    plt.close()


def plot_moving_averages(df):
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df["close"], label="Close", alpha=0.6)
    plt.plot(df.index, df["ma20"], label="MA20")
    plt.plot(df.index, df["ma50"], label="MA50")
    plt.title("Moving Averages")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend()
    plt.savefig("moving_averages.png", bbox_inches="tight")
    plt.close()


def plot_volatility(df):
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df["volatility20"], label="20-Day Volatility", color="orange")
    plt.title("Rolling Volatility (20-Day)")
    plt.xlabel("Time")
    plt.ylabel("Volatility")
    plt.grid(True)
    plt.legend()
    plt.savefig("rolling_volatility.png", bbox_inches="tight")
    plt.close()


def plot_sharpe(df):
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df["sharpe20"], label="20-Day Sharpe Ratio", color="green")
    plt.title("Rolling Sharpe Ratio (20-Day)")
    plt.xlabel("Time")
    plt.ylabel("Sharpe")
    plt.grid(True)
    plt.legend()
    plt.savefig("rolling_sharpe_ratio.png", bbox_inches="tight")
    plt.close()
def plot_trade_equity(df):
    plt.figure(figsize=(12, 5))
    plt.plot(df.index, df["trade_equity"], marker="o", linestyle="--")
    plt.title("Trade-by-Trade Equity")
    plt.grid(True)
    plt.savefig("trade_equity.png", bbox_inches="tight")
    plt.close()


def plot_exposure(df):
    plt.figure(figsize=(12, 3))
    plt.plot(df.index, df["exposure"], drawstyle="steps-post")
    plt.title("Exposure (Long/Short/Flat)")
    plt.grid(True)
    plt.savefig("exposure.png", bbox_inches="tight")
    plt.close()
