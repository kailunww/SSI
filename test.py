import xml.etree.ElementTree
import csv
import math
import pprint
import matplotlib.pyplot as plt
import numpy as np
import time

data = []
file_name = "data\AUDUSD_D1_HistoricalSSI.csv"
f = open(file_name, 'r')
for row in csv.DictReader(f):
    if row["SSI"]:
        for key in row.keys():
            if key != "Date":
                row[key] = float(row[key])
        ssi = row["SSI"]
        if ssi < 0:
            ssi = -1/ssi
        row["SSI_log"] = math.log(ssi)
        ts = time.strptime(row["Date"], "%d/%m/%Y %H:%M:%S")
        row["timestamp"] = time.mktime(ts)
        data.append(row)
f.close()
# pprint.pprint(data)
#
# t = [row["timestamp"] for row in data]
# s = [row["SSI_log"] for row in data]
#
# plt.plot(t, s)
#
# plt.xlabel('time (s)')
# plt.ylabel('voltage (mV)')
# plt.title('About as simple as it gets, folks')
# plt.grid(True)
# plt.savefig("test.png")
# plt.show()


class Trader:

    def __init__(self):
        self.margin = 0.02
        self.capital = 1000
        self.virtual = 0
        self.value = 0
        self.stock = 0
        self.trade_count = 0

    def buy(self, price, unit):
        self.virtual -= price * unit
        self.stock += unit
        self.value = price * self.stock
        self.trade_count += 1
        portfolio = self.stock * price
        print(self.net, self.virtual, self.value)
        if self.net < abs(portfolio) * self.margin:
            print("Not enough margin")
            print(self.net, abs(portfolio) * self.margin)
            input()
            raise ValueError("Not enough margin")

    def sell(self, price, unit):
        self.virtual += price * unit
        self.stock -= unit
        self.value = price * self.stock
        self.trade_count += 1
        portfolio = self.stock * price
        print(self.net, self.virtual, self.value)
        if self.net < abs(portfolio) * self.margin:
            print("Not enough margin")
            print(self.net, abs(portfolio) * self.margin)
            input()
            raise ValueError("Not enough margin")

    @property
    def net(self):
        return self.capital + self.value + self.virtual

trader = Trader()
last_ssi = 0
base_unit = 5000
data = sorted(data, key=lambda x: x["timestamp"])
trade_count = 0
logs = []
for index, row in enumerate(data):
    # print(index, row["timestamp"])
    ssi = row["SSI_log"]
    optimal_hold = -int(ssi/0.2) * base_unit
    diff = optimal_hold - trader.stock
    # last_ssi = row["SSI_log"]
    if diff > 0:
        price = row["Close, Bid"]
        unit = diff
        # unit = int(diff/0.1)
        print("buy @ %s for %s unit" % (price, unit), trader.capital, trader.stock, row["SSI_log"])
        trader.buy(price, unit)
        logs.append([trader.net, trader.stock])
    elif diff < 0:
        price = row["Close, Ask"]
        unit = -diff
        # unit = int(-diff/0.1)
        print("sell @ %s for %s unit" % (price, unit), trader.capital, trader.stock, row["SSI_log"])
        trader.sell(price, unit)
        logs.append([trader.net, trader.stock])
print(trader.capital, trader.stock, trader.trade_count)
current_price = data[-1]["Close, Bid"]
print(trader.net)
# net = trader.capital + trader.stock * current_price
# print(net)
final_value = trader.net
lowest_value = min([log[0] for log in logs])
time_span = data[-1]["timestamp"] - data[0]["timestamp"]
year_count = time_span/(365*60*60*24)
total_rr = (final_value - 1000) / 1000
print(total_rr)
print(year_count)
annual_rr = math.exp(math.log(total_rr)/year_count) - 1
print(annual_rr)
print(pow(1.2728, 9.6))
input()