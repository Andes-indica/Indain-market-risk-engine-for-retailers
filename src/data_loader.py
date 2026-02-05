# here only data feteching part 
import yfinance as yf
import pandas as pd
from pathlib import Path

def fetch_index_data(ticker, start="2010-01-01"):
    data = yf.download(ticker, start=start, progress=False)
    data.reset_index(inplace=True)
    # Flatten MultiIndex columns
    data.columns = [col[0] if col[1] == ticker or col[1] == '' else col[0] for col in data.columns]
    # Clean the data: drop rows with NaN in Date, convert numeric columns
    data = data.dropna(subset=['Date'])
    numeric_cols = ['Close', 'High', 'Low', 'Open', 'Volume']
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    data = data.dropna()  # Drop any rows with NaN after conversion
    return data

if __name__ == "__main__":
    nifty = fetch_index_data("^NSEI")
    banknifty = fetch_index_data("^NSEBANK")

    # Save into repo-root `data/raw/` so repo-root files are overwritten
    repo_root = Path(__file__).resolve().parent.parent
    out_dir = repo_root / "data" / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)

    nifty.to_csv(out_dir / "nifty.csv", index=False)
    banknifty.to_csv(out_dir / "banknifty.csv", index=False)
