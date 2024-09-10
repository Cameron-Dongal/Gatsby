import yfinance as yf
import pandas as pd
import pandas_ta as ta

today = '2024-09-05'

ticker = '^VIX'

def vix_sma(today, ticker):

    today = pd.to_datetime(today).tz_localize('UTC').tz_convert('America/New_York').normalize()

    day = today.weekday()
    if day == 0:
        yesterday = today - pd.DateOffset(3)
    else:
        yesterday = today - pd.DateOffset(1)



    df = yf.Ticker(ticker).history(period='5y', interval='1d')[['Close', 'Open', 'High', 'Volume', 'Low']]
    sma100 = df.ta.sma(close = 'close',length=100)
    df.index = df.index.normalize()



    print(sma100)
    return(sma100)

vix_sma(today, ticker)