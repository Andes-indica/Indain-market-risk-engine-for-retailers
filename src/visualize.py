
import matplotlib.pyplot as plt

# High-risk observations cluster before and during market drawdowns.    
def plot_price_with_risk(df):
    plt.figure(figsize=(12,6))
    plt.plot(df['Date'], df['Close'], alpha=0.7)

    plt.scatter(
        df['Date'],
        df['Close'],
        c=df['risk_score'],
        cmap='RdYlGn_r',
        s=10
    )

    plt.colorbar(label="Risk Score")
    plt.title("Index Price with Risk Overlay")
    plt.xlabel("Date")
    plt.ylabel("Index Level")
    plt.show()
    
# This chart shows how the system transitions between low, moderate, and high risk regimes over time.

def plot_risk_timeline(df):
    plt.figure(figsize=(12,4))
    plt.plot(df['Date'], df['risk_score'], color='black')

    plt.axhline(30, linestyle='--')
    plt.axhline(60, linestyle='--')

    plt.fill_between(df['Date'], 0, 30, alpha=0.1)
    plt.fill_between(df['Date'], 30, 60, alpha=0.1)
    plt.fill_between(df['Date'], 60, 100, alpha=0.1)

    plt.title("Market Risk Regimes")
    plt.ylabel("Risk Score")
    plt.xlabel("Date")
    plt.show()


# Expected Shortfall captures tail losses beyond the VaR threshold.
def plot_tail_risk(returns, var_95, cvar_95):
    plt.figure(figsize=(8,4))
    plt.hist(returns, bins=100, alpha=0.7)
    
    # x axis is returns for ex:- 0.05 --> 5% 
    #  y axis i the frequency of those returns in the data means how many days we have seen that return
    
    plt.axvline(var_95, linestyle='--', label='VaR 95%')# var shows that the with the 95% confidence level what is the maximum expected loss for a partcular day 
    plt.axvline(cvar_95, linestyle='-', label='CVaR 95%')# cvar shows that if the value crosses the var what is the expected loss on average for a particular day

    plt.legend()
    plt.title("Return Distribution with Tail Risk")
    plt.xlabel("Daily Returns")
    plt.ylabel("Frequency")
    plt.show()
    

# historical stress period plot ex:- covid period
# def plot_stress_period(df, start, end):
#     plt.figure(figsize=(12,5))
#     plt.plot(df['Date'], df['Close'])
#     plt.axvspan(start, end, alpha=0.3)
#     plt.title("Historical Stress Period")
#     plt.show()

