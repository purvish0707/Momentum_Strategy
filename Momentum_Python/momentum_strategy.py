import pandas as pd
import numpy as np

def run_momentum_strategy(prices: pd.DataFrame, lookback_period: int = 1, top_n: int = 20):
    """
    Runs a simple momentum strategy.
    
    Parameters:
    - prices: DataFrame of adjusted close prices (daily or monthly)
    - lookback_period: Lookback period for momentum calculation (in months if data is monthly)
    - top_n: Number of top stocks to select for the portfolio
    
    Returns:
    - portfolio_returns: A Series containing the monthly portfolio returns.
    """
    
    # Ensure data is sorted by index
    prices = prices.sort_index()
    
    # Resample to monthly frequency (last business day of the month)
    monthly_prices = prices.resample('BM').last()
    
    # Calculate returns over the lookback period
    momentum_returns = monthly_prices.pct_change(periods=lookback_period)
    
    # Shift returns by 1 to avoid look-ahead bias (we trade at the end of the month based on past returns)
    momentum_returns = momentum_returns.shift(1)
    
    # We will hold for 1 month. 
    # Calculate actual 1-month forward returns for all stocks
    forward_returns = monthly_prices.pct_change(periods=1).shift(-1)
    
    portfolio_returns = []
    index_dates = []
    
    # Iterate over each month to construct the portfolio
    for date in momentum_returns.index:
        # Get momentum returns for the date
        current_momentum = momentum_returns.loc[date].dropna()
        
        # If we don't have enough data to pick top_n stocks, skip the month
        if len(current_momentum) < top_n:
            continue
            
        # Rank stocks based on momentum and select top N
        top_stocks = current_momentum.nlargest(top_n).index
        
        # Get forward returns for the selected stocks for the *next* month
        if date in forward_returns.index:
            month_returns = forward_returns.loc[date, top_stocks]
            
            # Equal weight (1 / top_n)
            weights = np.ones(top_n) / top_n
            
            # Calculate portfolio return for the month
            port_ret = (month_returns * weights).sum()
            
            portfolio_returns.append(port_ret)
            index_dates.append(date)

    # Shift the dates by 1 month forward because the return is realized in the following month
    # Actually, the `date` is the end of the formation month, and `forward_returns` are for the month following it.
    # So the return should be stamped at the end of the holding month.
    
    # Let's create the final Series
    ret_series = pd.Series(portfolio_returns, index=index_dates)
    
    # We should align the index to the end of the holding month.
    # The 'date' currently represents the end of the formation month.
    # We shift the index forward by 1 month to represent the end of the holding period.
    if not ret_series.empty:
        ret_series.index = ret_series.index + pd.offsets.BMonthEnd(1)
    
    # Drop NaNs just in case
    ret_series = ret_series.dropna()
    
    return ret_series
