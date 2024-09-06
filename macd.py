import yfinance as yf
import pandas as pd
import pandas_ta as ta


today = '2024-09-05'

def macd(today):

    today = pd.to_datetime(today).tz_localize('UTC').tz_convert('America/New_York').normalize()

    day = today.weekday()
    if day == 0:
        yesterday = today - pd.DateOffset(3)
    else:
        yesterday = today - pd.DateOffset(1)

    print("\nTodays Date: ",today)


    df = yf.Ticker('SPY').history(period='5y', interval='1d')[['Close', 'Open', 'High', 'Volume', 'Low']]
    df.ta.macd(close='close',fast=12,slow=26,signal=9,append=True)
    df.index = df.index.normalize()

    macdh_today = df.loc[df.index == today,'MACDh_12_26_9']
    macdh_yesterday = df.loc[df.index == yesterday, 'MACDh_12_26_9']



    if not macdh_today.empty and not macdh_yesterday.empty:
        macdh_today = macdh_today.iloc[0]
        macdh_yesterday = macdh_yesterday.iloc[0]
        if macdh_today >= 0 and macdh_yesterday < 0:

            return "BUY"
        if macdh_today >= 0 and macdh_yesterday > 0:

            return "HOLD_LONG"
        if macdh_today <= 0 and macdh_yesterday > 0:

            return "SELL"
        if macdh_today <= 0 and macdh_yesterday < 0:

            return "HOLD_SHORT"
    else:

        return "NO_DATA"


macd(today)