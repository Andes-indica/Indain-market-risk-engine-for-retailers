import yfinance as yf

def fetch_fundamentals(market="NIFTY"):
    ticker = "^NSEI" if market == "NIFTY" else "^NSEBANK"

    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        'pe': info.get('trailingPE', 25),
        'pb': info.get('priceToBook', 3),
        'div_yield': (info.get('dividendYield', 0.02) * 100),
        'earnings_growth': (info.get('earningsQuarterlyGrowth', 0.1) * 100),
        'repo_rate': 6.5
    }
