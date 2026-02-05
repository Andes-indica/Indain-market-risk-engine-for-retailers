import streamlit as st
import pandas as pd

from src.features import add_features
from src.anomaly import zscore_anomaly, isolation_forest_anomaly, volatility_regime
from src.risk_engine import market_risk_score, risk_label
from src.risk_metrics import historical_var, historical_cvar, stress_test
# from src.visualize import (
#     plot_risk_timeline,
#     plot_price_with_risk,
#     plot_tail_risk
# )
from src.fundamentals import fetch_fundamentals
from src.visualize_interactive import (
    risk_timeline_interactive,
    price_risk_overlay_interactive,
    tail_risk_interactive
)


# APP CONFIG

st.set_page_config(
    page_title="Indian Market Risk Dashboard",
    layout="wide"
)

st.title(" Indian Market Risk Dashboard")
st.caption("Volatility • Anomalies • Fundamentals • Stress Testing")


# MARKET SELECTION

market = st.selectbox(
    "Select Market",
    ["NIFTY", "BANK NIFTY"]
)

data_path = (
    "data/raw/nifty.csv"
    if market == "NIFTY"
    else "data/raw/banknifty.csv"
)

df = pd.read_csv(data_path)
df["Date"] = pd.to_datetime(df["Date"])

# Process data with features and anomaly detection
df = add_features(df)
_, df["return_anomaly"] = zscore_anomaly(df["returns"])
df["vol_regime"] = volatility_regime(df["volatility_30"])
df = isolation_forest_anomaly(df, ["returns", "volatility_14", "volatility_30", "volume_zscore"])


# FUNDAMENTALS (DYNAMIC)

with st.spinner("Fetching latest fundamentals..."):
    fundamentals = fetch_fundamentals(market)

st.sidebar.header(" Fundamental Snapshot")
st.sidebar.metric("P/E Ratio", f"{fundamentals['pe']:.2f}")
st.sidebar.metric("P/B Ratio", f"{fundamentals['pb']:.2f}")
st.sidebar.metric("Dividend Yield (%)", f"{fundamentals['div_yield']:.2f}")
st.sidebar.metric("Earnings Growth (%)", f"{fundamentals['earnings_growth']:.2f}")
st.sidebar.metric("Repo Rate (%)", f"{fundamentals['repo_rate']:.2f}")


# RISK COMPUTATION (ENGINE)

df["risk_score"] = market_risk_score(df, fundamentals)

current_risk = df["risk_score"].iloc[-1]
risk_state = risk_label(current_risk)


# TOP SUMMARY METRICS

col1, col2, col3 = st.columns(3)

col1.metric("Current Risk Score", f"{current_risk:.1f}")
col2.metric("Risk Regime", risk_state)
col3.metric("Market", market)


# RISK TIMELINE

st.subheader(" Risk Regime Timeline (Last 1 Year)")
# plot_risk_timeline(df.tail(252))
st.plotly_chart(
    risk_timeline_interactive(df.tail(252)),
    use_container_width=True
)
# st.pyplot()


# PRICE + RISK OVERLAY

st.subheader(" Price with Risk Overlay (Last 1 Year)")
# plot_price_with_risk(df.tail(252))
st.plotly_chart(
    price_risk_overlay_interactive(df.tail(252)),
    use_container_width=True
)
# st.pyplot()


# DOWNSIDE RISK METRICS

returns = df["returns"].dropna()

var_95 = historical_var(returns)
cvar_95 = historical_cvar(returns)

covid_stress = stress_test(
    returns,
    start_date="2020-02-01",
    end_date="2020-04-30"
)

col4, col5, col6 = st.columns(3)
col4.metric("VaR (95%)", f"{var_95:.2%}")
col5.metric("CVaR (95%)", f"{cvar_95:.2%}")
col6.metric(
    "COVID Stress Loss",
    f"{covid_stress['cumulative_loss']:.2%}"
)


# TAIL RISK DISTRIBUTION

st.subheader(" Tail Risk Distribution")
# plot_tail_risk(returns, var_95, cvar_95)
st.plotly_chart(
    tail_risk_interactive(returns, var_95, cvar_95),
    use_container_width=True
)
# st.pyplot()


# FOOTER

st.markdown(
    """
    ---
    **Note:**  
    This dashboard is a presentation layer built on a validated risk engine.
    Market data, anomaly detection, fundamentals, and downside risk metrics
    are computed independently and consumed here for monitoring purposes.
    """
)
