import pandas as pd
import numpy as np

def add_features(df):
    df["returns"] = np.log(df["Close"] / df["Close"].shift(1))
    df["volatility_14"] = df["returns"].rolling(14).std() * np.sqrt(252)
    df["volatility_30"] = df["returns"].rolling(30).std() * np.sqrt(252)
    df["volume_zscore"] = (
        (df["Volume"] - df["Volume"].rolling(30).mean())
        / df["Volume"].rolling(30).std()
    )
    return df.dropna()
