from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta


output = TA_Handler(symbol='nvda',
                    screener='america',
                    exchange='nasdaq',
                    interval='5m')
print('symbol: '+output.symbol)
print(output.get_analysis().summary)
print(output.get_analysis().indicators)

symbols = [('AMEX','SPY'), ('NASDAQ','QQQ'), ('NASDAQ','NVDA'), ('NYSE','LLY'), ('NYSE','PLTR')]
print("tradingview API version: ",tradingview_ta.__version__)
for a in symbols:
    output = TA_Handler(symbol=a[1],
                        screener='america',
                        exchange=a[0],
                        interval='5m')
    print('Symbol: ',a[1])
    print(output.get_analysis().summary)

    
