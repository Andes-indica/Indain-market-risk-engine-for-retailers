# actually here we  are finding the historical downfall 
# After detecting elevated risk, the system quantifies potential downside using VaR, Expected Shortfall, and historical stress replay, aligning with institutional risk management practices.

# this will help to conclude the risk like “Market risk is HIGH, and historical data suggests potential downside of ~3% in a day and ~20% during extreme stress.”
def max_drawdown(close):
    cumulative = close / close.iloc[0]
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()
import numpy as np

def historical_var(returns, confidence=0.95):
    
    # Historical Value at Risk (VaR)
    # At a given confidence level, the maximum expected loss over a specified period.
    
    returns = returns.dropna()
    return np.percentile(returns, (1 - confidence) * 100)

def historical_cvar(returns, confidence=0.95):
    
    #  Conditional Value at Risk (Expected Shortfall) 
    # if losess exceed then how bad they can get on average
    
    var = historical_var(returns, confidence)
    return returns[returns <= var].mean()

def stress_test(returns, start_date, end_date):
    
    # Replay historical stress period 
    #  e.g., 2008 financial crisis or 2020 COVID crash
    
    stress_returns = returns.loc[start_date:end_date]
    cumulative_loss = (1 + stress_returns).prod() - 1
    max_loss = stress_returns.min()
    
    return {
        "cumulative_loss": cumulative_loss,
        "worst_day": max_loss
    }
