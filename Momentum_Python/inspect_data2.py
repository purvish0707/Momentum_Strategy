import yfinance as yf
data = yf.download(["RELIANCE.NS", "TCS.NS"], start="2015-01-01", end="2023-12-31")
print(data.columns)
