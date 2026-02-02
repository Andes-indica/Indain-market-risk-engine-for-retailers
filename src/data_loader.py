# here only data feteching part 
import yfinance as yf
import pandas as pd

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

    nifty.to_csv("data/raw/nifty.csv", index=False)
    banknifty.to_csv("data/raw/banknifty.csv", index=False)
