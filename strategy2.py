from read import parse_csv
from model import Trader, Log, LogManager, Bar, Result
import math


bars = parse_csv("data\AUDUSD_D1_HistoricalSSI.csv")
# bars = parse_csv("data\GBPUSD_D1_HistoricalSSI.csv")
# bars = parse_csv("data\EURUSD_D1_HistoricalSSI.csv")
base_unit = 100000
capital = 10000
margin = 0.02
trade_count = 0
MAX_LIMIT = 8
IGNORE = 0
THRESHOLD = 3
trader = Trader(capital=capital, margin=margin)
logs = LogManager()
for bar in bars.bars:
    ssi = bar.ssi
    if trader.stock > 0:
        if ssi >= -THRESHOLD:
            trader.close(bar)
            logs.add(Log(
                timestamp=bar.timestamp,
                equity=trader.equity,
                stock=trader.stock,
            ))
    elif trader.stock < 0:
        if ssi <= -THRESHOLD:
            trader.close(bar)
            logs.add(Log(
                timestamp=bar.timestamp,
                equity=trader.equity,
                stock=trader.stock,
            ))
    if trader.stock == 0:
        if ssi >= THRESHOLD:
            unit = base_unit
            trader.sell(bar, unit)
            logs.add(Log(
                timestamp=bar.timestamp,
                equity=trader.equity,
                stock=trader.stock,
            ))
        elif ssi <= -THRESHOLD:
            unit = base_unit
            trader.buy(bar, unit)
            logs.add(Log(
                timestamp=bar.timestamp,
                equity=trader.equity,
                stock=trader.stock,
            ))
trader.update_value(bars.last().close_bid)
result = Result(
    capital=capital,
    equity=trader.equity,
    trade_count=trader.trade_count,
    year_count=bars.year_count,
    lowest=logs.lowest(),
    highest=logs.highest(),
)
result.output()
