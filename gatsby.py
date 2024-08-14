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
        "symbol": "SPY",
        "quantity": 20,
        "side": "buy"
    }
    
    def initialize(self, symbol="SPY"):
        self.sleeptime = "5M"
        self.last_trade = "sell"
        self.minutes_before_closing = 8

    def on_trading_iteration(self):

        output = TA_Handler(symbol='SPY',
                    screener='america',
                    exchange='AMEX',
                    interval='5m')
     
        rec5 = output.get_analysis().summary["RECOMMENDATION"]

        symbol = self.parameters["symbol"]
        quantity = self.parameters["quantity"]
        side = self.parameters["side"]

        if "BUY" or "STRONG_BUY" in rec5 and self.last_trade == "sell":
            order = self.create_order(symbol, quantity, side)
            self.last_trade = "buy"
            self.parameters["side"] = "sell"
            self.submit_order(order)
        elif "SELL" or "STRONG_SELL" in rec5 and self.last_trade == "buy":
            order = self.create_order(symbol, quantity, side)
            self.parameters["side"]="buy"
            self.last_trade="sell"
            self.submit_order(order)   
            
trader = Trader()
broker = Alpaca(ALPACA_CONFIG)
strategy = TestStrategy(broker=broker, parameters={"symbol":"SPY"})

trader.add_strategy(strategy)
trader.run_all()

