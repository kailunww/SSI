import math
from datetime import datetime
import setting


class Log:

    def __init__(self, timestamp, equity, stock):
        self.timestamp = timestamp
        self.equity = equity
        self.stock = stock


class LogManager:

    def __init__(self):
        self.logs = []

    def add(self, log: Log):
        self.logs.append(log)

    def lowest(self):
        return min([log.equity for log in self.logs])

    def highest(self):
        return max([log.equity for log in self.logs])


class Bar:

    def __init__(self, timestamp, open_bid, open_ask, close_bid, close_ask, ssi):
        self.timestamp = timestamp
        self.open_bid = open_bid
        self.open_ask = open_ask
        self.close_bid = close_bid
        self.close_ask = close_ask
        self.ssi = ssi


class BarManager:

    def __init__(self):
        self.bars = []

    def add(self, bar: Bar):
        self.bars.append(bar)

    def sort(self):
        self.bars = sorted(self.bars, key=lambda x: x.timestamp)

    def first(self) -> Bar:
        return self.bars[0]

    def last(self) -> Bar:
        return self.bars[-1]

    @property
    def year_count(self):
        time_span = self.last().timestamp - self.first().timestamp
        return time_span/(365*60*60*24)


class Trader:

    def __init__(self, capital=setting.CAPITAL, margin=setting.MARGIN):
        self.capital = capital
        self.margin = margin
        self.virtual = 0
        self.value = 0
        self.stock = 0
        self.trade_count = 0

    def buy(self, bar: Bar, unit):
        price = bar.close_ask
        ex_date = datetime.fromtimestamp(bar.timestamp)
        print(ex_date.isoformat(), "buy @ %s for %s unit" % (price, unit), self.capital, self.stock, bar.ssi)
        self.virtual -= price * unit
        self.stock += unit
        self.update_value(bar)
        self.trade_count += 1
        print(self.equity, self.virtual, self.value)
        if self.equity < abs(self.value) * self.margin:
            print("Not enough margin")
            print(self.equity, abs(self.value) * self.margin)
            raise ValueError("Not enough margin")

    def sell(self, bar: Bar, unit):
        price = bar.close_bid
        ex_date = datetime.fromtimestamp(bar.timestamp)
        print(ex_date.isoformat(), "sell @ %s for %s unit" % (price, unit), self.capital, self.stock, bar.ssi)
        self.virtual += price * unit
        self.stock -= unit
        self.update_value(bar)
        self.trade_count += 1
        print(self.equity, self.virtual, self.value)
        if self.equity < abs(self.value) * self.margin:
            print("Not enough margin")
            print(self.equity, abs(self.value) * self.margin)
            raise ValueError("Not enough margin")

    def close(self, bar: Bar):
        print("Close")
        if self.stock > 0:
            self.sell(bar, self.stock)
        elif self.stock < 0:
            self.buy(bar, -self.stock)

    def update_value(self, bar: Bar):
        if self.stock > 0:
            self.value = self.stock * bar.close_bid
        else:
            self.value = self.stock * bar.close_ask

    @property
    def equity(self):
        return self.capital + self.value + self.virtual


class Result:

    def __init__(self, trader: Trader, year_count, logs: LogManager):
        self.capital = trader.capital
        self.equity = trader.equity
        self.trade_count = trader.trade_count
        self.year_count = year_count
        self.lowest = logs.lowest()
        self.highest = logs.highest()
        self.ror = (self.equity - self.capital) / self.capital
        self.annual_ror = math.exp(math.log(1 + self.ror)/year_count) - 1

    def output(self):
        for key, value in vars(self).items():
            print("%s = %s" % (key, value))
