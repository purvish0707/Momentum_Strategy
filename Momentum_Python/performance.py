import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_cagr(returns: pd.Series) -> float:
    """
    Calculates Compound Annual Growth Rate (CAGR).
    Assumes monthly returns as input.
    """
    # Number of years
    # Since returns are monthly, total months is len(returns)
    years = len(returns) / 12
    
    # Cumulative return
    cumulative_return = (1 + returns).prod()
    
    if years == 0:
        return 0.0
        
    cagr = (cumulative_return ** (1 / years)) - 1
    return cagr

def calculate_annualized_volatility(returns: pd.Series) -> float:
    """
    Calculates annualized volatility from monthly returns.
    """
    # Volatility is std deviation of returns scaled by sqrt(12) for monthly data
    monthly_vol = returns.std()
    annualized_vol = monthly_vol * np.sqrt(12)
    return annualized_vol

def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.07) -> float:
    """
    Calculates the Annualized Sharpe Ratio.
    risk_free_rate is assumed to be an annual rate (e.g. 7% -> 0.07).
    """
    # Convert annual risk free rate to monthly
    monthly_rf = (1 + risk_free_rate) ** (1/12) - 1
    
    # Excess returns
    excess_returns = returns - monthly_rf
    
    # Sharpe ratio
    # Mean excess return / std dev of excess return, annualized
    monthly_sharpe = excess_returns.mean() / excess_returns.std()
    
    annualized_sharpe = monthly_sharpe * np.sqrt(12)
    return annualized_sharpe

def plot_equity_curve(returns: pd.Series, title: str = "Strategy Cumulative Returns"):
    """
    Plots the equity curve of the strategy.
    """
    cumulative_returns = (1 + returns).cumprod()
    
    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_returns.index, cumulative_returns, label="Strategy")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Value (Base 1)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("equity_curve.png")
    print("Plot saved to 'equity_curve.png'.")
