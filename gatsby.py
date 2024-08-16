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
    parameters = {
        "symbol": "BTC/USD",#change to spy / btc/usd
        "quantity": .1,
        "side": "buy"
    }

    
    def initialize(self, symbol="BTC/USD"):#change to spy / btc/usd
        self.sleeptime = "1M"
        self.last_trade = "sell"
        #self.minutes_before_closing = 8
        self.set_market('24/7') #delete when not using crypto to test afterhours, and replace btc symbols and exchange with spy and amex

    def on_trading_iteration(self):
        
        print(" ")

        output = TA_Handler(symbol='btcusdc', #change to spy / btcusdc
                    screener='crypto', #change to america / crytpo
                    exchange='kraken', #change to amex / kraken
                    interval='1m')
     
        rec5 = output.get_analysis().summary["RECOMMENDATION"]

        symbol = self.parameters["symbol"]
        quantity = self.parameters["quantity"]

        position = self.get_position(symbol)

        print(symbol, " : ", output.get_analysis().summary)
        print(rec5, " recommended, checking position...")


        print("Position:", position)

        if rec5 == "BUY" or rec5 == "STRONG_BUY":
            if self.last_trade == "sell":
                print("Entering position...")
                order = self.create_order(symbol, quantity, "buy")
                self.last_trade = "buy"
                self.parameters["side"] = "sell"
                self.submit_order(order)

        elif rec5 == "SELL" or rec5 == "STRONG_SELL":
            if self.last_trade == "buy":
                print("Exiting posiition")
                order = self.create_order(symbol, quantity, "buy")
                self.parameters["side"] = "buy"
                self.last_trade = "sell"
                self.submit_order(order)
        


        
        


        
    def on_abrupt_closing(self):
        self.log_message("Abrupt closing")
        self.sell_all()
            
trader = Trader()
broker = Alpaca(ALPACA_CONFIG)
strategy = TestStrategy(broker=broker, parameters={"symbol":"BTC/USD"}) #change to spy / btc/usd

trader.add_strategy(strategy)
trader.run_all()

