from data_loader import get_nifty500_symbols, download_historical_data
from momentum_strategy import run_momentum_strategy
symbols = get_nifty500_symbols()[:20]
prices = download_historical_data(symbols, "2015-01-01", "2023-12-31")
print("prices shape:", prices.shape)
print("prices head:\n", prices.head())
import pandas as pd
prices = prices.sort_index()
monthly_prices = prices.resample('BM').last()
momentum_returns = monthly_prices.pct_change(periods=1)
momentum_returns = momentum_returns.shift(1)
date = momentum_returns.index[2]
print("Date:", date)
current_momentum = momentum_returns.loc[date].dropna()
print("len current_momentum:", len(current_momentum))
