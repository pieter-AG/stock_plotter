import pandas_datareader.nasdaq_trader as nqt
all_tickers = nqt.get_nasdaq_symbols(retry_count=3, timeout=30, pause=None)
print(all_tickers)