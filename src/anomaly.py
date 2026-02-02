import numpy as np
from sklearn.ensemble import IsolationForest
def zscore_anomaly(series, window=30, threshold=2.5):
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()

    zscore = (series - rolling_mean) / rolling_std
    anomaly = np.abs(zscore) > threshold

    return zscore, anomaly

def volatility_regime(vol_series, window=60):
    long_term_avg = vol_series.rolling(window).mean()
    regime_shift = vol_series > (1.5 * long_term_avg)
    return regime_shift



def isolation_forest_anomaly(df, feature_cols):
    model = IsolationForest(
        n_estimators=100,
        contamination=0.02,
        random_state=42
    )

    X = df[feature_cols]
    preds = model.fit_predict(X)

    # -1 = anomaly, 1 = normal
    df["if_anomaly"] = preds == -1
    return df
