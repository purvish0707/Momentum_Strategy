import pandas as pd
import yfinance as yf
import requests
import io

def get_nifty500_symbols():
    """
    Fetches the latest NIFTY 500 symbols from NSE India website.
    Since historical constituents are hard to get freely, we use the current ones.
    """
    url = 'https://archives.nseindia.com/content/indices/ind_nifty500list.csv'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        symbols = df['Symbol'].tolist()
        
        # Append .NS for Yahoo Finance
        yahoo_symbols = [f"{sym}.NS" for sym in symbols]
        return yahoo_symbols
    except Exception as e:
        print(f"Error fetching NIFTY 500 symbols: {e}")
        print("Falling back to a small subset for demonstration purposes...")
        # Fallback subset just in case
        return ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS', 
                'HINDUNILVR.NS', 'SBI.NS', 'ITC.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS']

def download_historical_data(symbols, start_date, end_date):
    """
    Downloads historical adjusted closing prices for the given symbols.
    """
    print(f"Downloading data for {len(symbols)} symbols from {start_date} to {end_date}...")
    # Use auto_adjust=False and get 'Adj Close' to be explicit, or just get 'Adj Close' if available.
    data = yf.download(symbols, start=start_date, end=end_date, progress=True)
    
    if isinstance(data.columns, pd.MultiIndex):
        # Multiple tickers
        # With auto_adjust=True (default in new yfinance), 'Close' is the adjusted close.
        if 'Close' in data.columns.levels[0]:
            adj_close = data['Close']
        elif 'Adj Close' in data.columns.levels[0]:
            adj_close = data['Adj Close']
        else:
            adj_close = data.iloc[:, 0] # fallback
    else:
        # Single ticker
        adj_close = data['Adj Close'].to_frame(symbols[0])
        
    return adj_close
