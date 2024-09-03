from lumibot.traders import Trader
from lumibot.brokers import Alpaca
from lumibot.strategies.strategy import Strategy
from lumibot.backtesting import YahooDataBacktesting


from datetime import datetime

from config import API_URL,API_SECRET,API_KEY

ALPACA_CONFIG = {
    "API_KEY": API_KEY,
    "API_SECRET":API_SECRET,
    "PAPER":  True
}

from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta

class TestStrategy(Strategy):

    def initialize(self, symbol="SPY", risk:float=.5):#change to spy / btc/usd
        self.symbol = symbol
        self.sleeptime = "1D"
        self.last_trade = "sell"
        self.risk = risk
        #self.minutes_before_closing = 8
        self.set_market('24/7') #delete when not using crypto to test afterhours, and replace btc symbols and exchange with spy and amex

    def technicals(self):
        output = TA_Handler(symbol='spy', #change to spy / btcusdc
                    screener='america', #change to america / crytpo
                    exchange='amex', #change to amex / kraken
                    interval='1d')
     
        recommendation = output.get_analysis().summary["RECOMMENDATION"]
        return recommendation

    def sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.risk / last_price,0)
        return cash, last_price, quantity
    
    def on_trading_iteration(self):

        technicals = self.technicals()

        cash, last_price, quantity = self.sizing()
        symbol = self.symbol


        if cash > last_price:

            if technicals == "BUY" or technicals == "STRONG_BUY":
                if self.last_trade == "sell":
                    self.sell_all()
                order = self.create_order(
                    symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price = last_price*1.6,
                    stop_loss_price = last_price*0.95
                    )
                self.last_trade = "buy"
                self.submit_order(order)

            elif technicals == "SELL" or technicals == "STRONG_SELL":
                if self.last_trade == "buy":
                    self.sell_all()
                order = self.create_order(
                    symbol,
                    quantity,
                    "sell",
                    type="bracket",
                    take_profit_price = last_price*.4,
                    stop_loss_price = last_price *1.05
                )
                self.last_trade = "sell"
                self.submit_order(order)
         
    def on_abrupt_closing(self):
        self.log_message("Abrupt closing")
        self.sell_all()
            
start_date = datetime(2022,1,1)
end_date = datetime(2024, 8, 21)

broker = Alpaca(ALPACA_CONFIG)

strategy = TestStrategy(name='teststrat', broker=broker, parameters={"symbol":"SPY", "cash_at_risk":.5})     
strategy.backtest(YahooDataBacktesting, start_date,end_date,parameters={"symbol":"SPY","cash_at_risk":.5})  

#uncomment following to run live

#trader = Trader()
#trader.add_strategy(strategy)
#trader.run_all()

