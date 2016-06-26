from read import parse_csv
from model import Trader, Log, LogManager, Bar, Result
import math


bars = parse_csv("data\AUDUSD_D1_HistoricalSSI.csv")
# bars = parse_csv("data\GBPUSD_D1_HistoricalSSI.csv")
# bars = parse_csv("data\EURUSD_D1_HistoricalSSI.csv")
base_unit = 5000
capital = 1000
margin = 0.02
trade_count = 0
MAX_LIMIT = 8
IGNORE = 0
trader = Trader(capital=capital, margin=margin)
logs = LogManager()
for bar in bars.bars:
    ssi = bar.ssi
    # if abs(ssi) < IGNORE:
    #     continue
    # if ssi > 0:
    #     adjusted_ssi = ssi - IGNORE
    # else:
    #     adjusted_ssi = ssi + IGNORE
    optimal_hold = -int(ssi/0.2)
    # if optimal_hold > MAX_LIMIT:
    #     optimal_hold = MAX_LIMIT
    # elif optimal_hold < -MAX_LIMIT:
    #     optimal_hold = -MAX_LIMIT
    optimal_hold *= base_unit
    diff = optimal_hold - trader.stock
    # last_ssi = row["SSI_log"]
    if diff > 0:
        price = bar.close_ask
        unit = diff
        print("buy @ %s for %s unit" % (price, unit), trader.capital, trader.stock, bar.ssi)
        trader.buy(price, unit)
        logs.add(Log(
            timestamp=bar.timestamp,
            equity=trader.equity,
            stock=trader.stock,
        ))
    elif diff < 0:
        price = bar.close_bid
        unit = -diff
        print("sell @ %s for %s unit" % (price, unit), trader.capital, trader.stock, bar.ssi)
        trader.sell(price, unit)
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
input()