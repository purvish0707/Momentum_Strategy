import pandas as pd
from data_loader import get_nifty500_symbols, download_historical_data

symbols = get_nifty500_symbols()
# take first 10 for quick test
prices = download_historical_data(symbols[:20], "2015-01-01", "2023-12-31")
print(prices.head())
print("Shape:", prices.shape)
