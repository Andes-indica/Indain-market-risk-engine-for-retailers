#  Indian Market Risk Engine

A multi-factor market risk assessment system for Indian equity indices (NIFTY & BANKNIFTY), built using Python, financial risk metrics, anomaly detection, and an interactive dashboard.

---

##  Overview

This project implements a **systematic risk engine** designed to quantify market stress in Indian equity markets using historical price data and dynamically fetched fundamentals.

Instead of predicting prices or generating trade signals, the system focuses on **risk monitoring**, explainability, and robustness.

---

##  Motivation

Markets often look stable on the surface while risk builds underneath.

This project answers:

> **How can market risk be quantified objectively using data rather than intuition or technical indicators?**

The emphasis is on **risk regimes, tail risk, and abnormal behavior**, not speculation.

---

##  Core Concepts

### Finance
- Volatility clustering
- Drawdowns
- Value at Risk (VaR)
- Conditional VaR (CVaR / Expected Shortfall)
- Market risk regimes
- Fundamentals-based risk adjustment

### Data Science & ML
- Time-series feature engineering
- Isolation Forest (unsupervised anomaly detection)
- Rolling window statistics

### Engineering
- Modular architecture
- Separation of logic and visualization
- Interactive dashboards with Streamlit & Plotly

---

##  Tech Stack

### Programming & Data
- Python 3
- NumPy
- Pandas

### Machine Learning
- Scikit-learn (Isolation Forest)

### Financial Risk Metrics
- Volatility (rolling)
- Drawdowns
- Value at Risk (VaR)
- Conditional VaR (CVaR)

### Visualization
- Matplotlib (static analysis)
- Plotly (interactive charts)

### Dashboard
- Streamlit

### Data Sources
- Historical market data (CSV)
- Dynamically fetched fundamental indicators

```
##  System Architecture
The system follows a modular, layered architecture:
Market Data (CSV + Fundamentals)
        ↓
Feature Engineering
        ↓
Risk Engine (Multi-factor)
        ↓
Risk Scores & Regimes
        ↓
Visualization Layer
        ↓
Interactive Dashboard

```
### Module Responsibilities

- `risk_engine.py`
  - Computes volatility, drawdowns, tail risk
  - Runs anomaly detection
  - Aggregates final risk score (0–100)

- `fundamentals.py`
  - Dynamically fetches and processes fundamental indicators
  - Supplies macro/valuation context to the risk engine

- `utils.py`
  - Reusable statistical helpers
  - Keeps engine logic clean and modular

- `visualize.py`
  - Static plots for validation and analysis

- `visualize_interactive.py`
  - Interactive Plotly charts for dashboard exploration

- `dashboard.py`
  - Streamlit interface
  - Consumes computed outputs (no business logic)



    ##  Architecture Diagram

```mermaid
flowchart TD
    A[Market Data CSV Files]
    B[Fundamentals API Data]

    A --> C[Feature Engineering]
    B --> D[Fundamental Processing]

    C --> E[Risk Engine]
    D --> E

    E --> F[Risk Metrics]
    F --> G[Final Risk Score]

    G --> H[Visualization Layer]
    H --> I[Streamlit Dashboard]
