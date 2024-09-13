import yfinance as yf
import pandas as pd
import pandas_ta as ta







def vix_sma(today):



    ticker = '^VIX'

    one_day = today - pd.DateOffset(1)
    two_days = today - pd.DateOffset(2)
    three_days = today - pd.DateOffset(3)
    four_days = today - pd.DateOffset(4)
    five_days = today - pd.DateOffset(5)

    counter = 0

    df = yf.Ticker(ticker).history(period='5y', interval='1d')[['Close', 'Open', 'High', 'Volume', 'Low']]
    df.ta.sma(close = 'close',length=100,append=True)
    df = df.ffill()
    df.index = df.index.normalize()

    sma100 = df.loc[df.index == today,'SMA_100']
    vix = df.loc[df.index == today,'Close']

    sma100_1 = df.loc[df.index == one_day,'SMA_100']
    vix_1 = df.loc[df.index == one_day,'Close']

    sma100_2 = df.loc[df.index == two_days,'SMA_100']
    vix_2 = df.loc[df.index == two_days,'Close']

    sma100_3 = df.loc[df.index == three_days,'SMA_100']
    vix_3 = df.loc[df.index == three_days,'Close']

    sma100_4 = df.loc[df.index ==four_days,'SMA_100']
    vix_4 = df.loc[df.index == four_days,'Close']

    sma100_5 = df.loc[df.index == five_days,'SMA_100']
    vix_5 = df.loc[df.index == five_days,'Close']




    if not sma100.empty and not vix.empty:

        sma100 = sma100.iloc[0]
        vix = vix.iloc[0]
        sma100_1 = sma100_1.iloc[0]
        vix_1 = vix_1.iloc[0]
        sma100_2 = sma100_2.iloc[0]
        vix_2 = vix_2.iloc[0]
        sma100_3 = sma100_3.iloc[0]
        vix_3 = vix_3.iloc[0]
        sma100_4 = sma100_4.iloc[0]
        vix_4 = vix_4.iloc[0]
        sma100_5 = sma100_5.iloc[0]
        vix_5 = vix_5.iloc[0]

        if sma100 <= vix:
            counter +=1
        if sma100_1 <= vix_1:
            counter +=1
        if sma100_2 <= vix_2:
            counter +=1
        if sma100_3 <= vix_3:
            counter +=1
        if sma100_4 <= vix_4:
            counter +=1
        if sma100_5 <= vix_5:
            counter +=1  

        if counter >= 3:
            return True
        else:
            return False          
    else:
        return None

