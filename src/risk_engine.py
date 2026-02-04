import numpy as np
from .fundamentals import fetch_fundamentals
def normalize_boolean(signal):
    """Convert boolean anomaly signal to risk score"""
    return signal.astype(int)



# 2. MARKET STRESS (FINANCE)


def volatility_stress(vol_series, window=252):
    """
    Measures how extreme current volatility is
    relative to long-term historical behavior.
    """
    long_term_mean = vol_series.rolling(window).mean()
    stress = vol_series / long_term_mean
    stress = stress.clip(upper=3)  # cap extreme noise
    return stress.fillna(0)



#  FUNDAMENTAL RISK (CORE FINANCE)


def fundamental_risk_score(fundamentals):
    """
    fundamentals = {
        'pe': float,
        'pb': float,
        'div_yield': float,
        'earnings_growth': float,
        'repo_rate': float
    }
    """

    pe_risk = min(fundamentals['pe'] / 30, 1)
    pb_risk = min(fundamentals['pb'] / 5, 1)
    div_risk = 1 - min(fundamentals['div_yield'] / 3, 1)
    growth_risk = 1 - min(fundamentals['earnings_growth'] / 15, 1)
    rate_risk = min(fundamentals['repo_rate'] / 8, 1)

    return np.mean([pe_risk, pb_risk, div_risk, growth_risk, rate_risk])



# 4. TOTAL MARKET RISK ENGINE


def market_risk_score(df, fundamentals=None):
    """
    Final Risk Score (0-100)
    Assumes df contains:
    - volatility_30
    - return_anomaly
    - if_anomaly

    fundamentals: dict or None (if None, will fetch real-time)
    """

    # Fetch fundamentals if not provided
    if fundamentals is None:
        fundamentals = fetch_fundamentals()

    # Market stress
    vol_score = volatility_stress(df["volatility_30"])

    # ML anomaly signals
    ret_score = normalize_boolean(df["return_anomaly"])
    ml_score  = normalize_boolean(df["if_anomaly"])

    # Fundamental layer
    fund_score = fundamental_risk_score(fundamentals)

    raw_score = (
        0.35 * vol_score +
        0.25 * ret_score +
        0.20 * ml_score +
        0.20 * fund_score
    )

    # Stable scaling (robust)
    scaled_score = np.clip(raw_score * 25, 0, 100)
    return scaled_score.fillna(0)



#  RISK LABELS


def risk_label(score):
    if score < 30:
        return "Low Risk"
    elif score < 60:
        return "Moderate Risk"
    else:
        return "High Risk"
