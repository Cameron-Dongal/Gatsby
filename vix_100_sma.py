import yfinance as yf
import pandas as pd
import pandas_ta as ta







def vix_sma(today):



    ticker = '^VIX'


    df = yf.Ticker(ticker).history(period='5y', interval='1d')[['Close', 'Open', 'High', 'Volume', 'Low']]
    df.ta.sma(close = 'close',length=100,append=True)
    df.index = df.index.normalize()

    sma100 = df.loc[df.index == today,'SMA_100']
    vix = df.loc[df.index == today,'Close']


    if not sma100.empty and not vix.empty:

        sma100 = sma100.iloc[0]
        vix = vix.iloc[0]

        if sma100 <= vix:
            print("VIX is above the SMA")
            return True
        if vix < sma100:
            print("VIX is below the SMA")
            return False
    else:
        return None

