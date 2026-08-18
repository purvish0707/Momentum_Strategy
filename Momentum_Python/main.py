import pandas as pd
from data_loader import get_nifty500_symbols, download_historical_data
from momentum_strategy import run_momentum_strategy
from performance import calculate_cagr, calculate_annualized_volatility, calculate_sharpe_ratio, plot_equity_curve

def main():
    from datetime import datetime
    
    print("Fetching NIFTY 500 symbols...")
    symbols = get_nifty500_symbols()
    
    print(f"Total symbols fetched: {len(symbols)}")
    
    # Backtest period
    start_date = "2000-01-01"
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    print(f"Downloading historical data from {start_date} to {end_date}...")
    prices = download_historical_data(symbols, start_date, end_date)
    
    print("Running momentum strategy...")
    # 1-month lookback, top 20 stocks
    portfolio_returns = run_momentum_strategy(prices, lookback_period=1, top_n=20)
    
    if portfolio_returns.empty:
        print("No returns generated. Please check the data or date range.")
        return
        
    print("\n--- Strategy Performance ---")
    cagr = calculate_cagr(portfolio_returns)
    volatility = calculate_annualized_volatility(portfolio_returns)
    sharpe = calculate_sharpe_ratio(portfolio_returns, risk_free_rate=0.068) # 6.8% risk-free rate (current India 10Y yield)
    
    print(f"CAGR:               {cagr * 100:.2f}%")
    print(f"Annualized Vol:     {volatility * 100:.2f}%")
    print(f"Sharpe Ratio (6.8% RF): {sharpe:.2f}")
    
    print("\nGenerating equity curve plot...")
    plot_equity_curve(portfolio_returns)
    print("Backtest completed successfully.")

if __name__ == "__main__":
    main()
