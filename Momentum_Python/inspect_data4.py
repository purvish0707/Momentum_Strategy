import yfinance as yf
data = yf.download(["RELIANCE.NS", "ACMESOLAR.NS", "TCS.NS"], start="2015-01-01", end="2023-12-31")
print(data.columns)
print(data['Close'].head())
