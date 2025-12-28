def run_batch_backtests(strategy, csv_paths, params):
    results = []
    for path in csv_paths:
        bt = BacktestEngine(strategy=strategy, data=load_csv(path), params=params)
        stats = bt.run()
        stats["symbol"] = extract_symbol(path)
        results.append(stats)
    return pd.DataFrame(results)
def rank_results(df, metric="CAGR"):
    df = df.sort_values(metric, ascending=False)
    df["rank"] = range(1, len(df)+1)
    return df
score = 0.4*CAGR + 0.2*WinRate + 0.2*Expectancy + 0.2*Sharpe

params = {
    "lookback": [10, 20, 50],
    "atr_mult": [1.5, 2.0, 3.0],
    "regime_filter": [True, False]
}
def optimize_params(strategy, data, param_grid):
    best = None
    best_score = -999
    for combo in itertools.product(*param_grid.values()):
        p = dict(zip(param_grid.keys(), combo))
        stats = BacktestEngine(strategy, data, p).run()
        score = stats["CAGR"] - stats["MaxDD"]
        if score > best_score:
            best_score = score
            best = (p, stats)
    return best
if params["regime_filter"]:
    regime = price > sma(price, 200)
    if not regime:
        return  # skip trade
atr = ATR(data, 14)
vol_ok = atr < atr.rolling(200).quantile(0.8)
if not vol_ok:
    return
portfolio = equity_curves.mean(axis=1)
weight_i = 1 / vol_i
weights = weight_i / sum(weight_i)
portfolio = (equity_curves * weights).sum(axis=1)
win_rate = wins / total_trades
avg_R = trade_log["R"].mean()
stats["win_rate"] = win_rate
stats["expectancy"] = expectancy
stats["avg_R"] = avg_R
