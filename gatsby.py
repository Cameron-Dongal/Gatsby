from lumibot.traders import Trader
from lumibot.brokers import Alpaca
from lumibot.strategies.strategy import Strategy
from lumibot.backtesting import YahooDataBacktesting

from datetime import datetime

from tradingview_ta import TA_Handler, Interval, Exchange
import tradingview_ta

API_KEY = "PKB6179NROHZUW4OM9UN"
API_SECRET = "xnAZ6rDWg8yrvdwl1V3PnkIBWGcWt0ikKWSdJCY2"
API_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CONFIG = {
    "API_KEY": API_KEY,
    "API_SECRET":API_SECRET,
    "PAPER":  True
}

class TestStrategy(Strategy):
    parameters = {
        "symbol": "SPY",
        "quantity": 1,
        "side": "buy"
    }

    def initialize(self, symbol=""):
        self.sleeptime = "180M"

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        quantity = self.parameters["quantity"]
        side = self.parameters["side"]
        order = self.create_order(symbol, quantity, side)
        self.submit_order(order)

trader = Trader()
broker = Alpaca(ALPACA_CONFIG)
strategy = TestStrategy(broker=broker, parameters={"symbol": "SPY"})

backtesting_start = datetime(2021, 1, 1)
backtesting_end = datetime(2024, 8, 9)

strategy.backtest(YahooDataBacktesting,backtesting_start,backtesting_end,parameters={"symbol": "SPY"})

#trader.add_strategy(strategy)
#trader.run_all()


