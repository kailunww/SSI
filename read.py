import csv
import math
import time
from model import Bar, BarManager


def parse_csv(file_name):
    bars = BarManager()
    # file_name = "data\AUDUSD_D1_HistoricalSSI.csv"
    f = open(file_name, 'r')
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    key_open_ask = [field for field in fields if "open" in field.lower() and "ask" in field.lower()][0]
    key_open_bid = [field for field in fields if "open" in field.lower() and "bid" in field.lower()][0]
    key_close_ask = [field for field in fields if "close" in field.lower() and "ask" in field.lower()][0]
    key_close_bid = [field for field in fields if "close" in field.lower() and "bid" in field.lower()][0]
    key_ssi = [field for field in fields if "ssi" in field.lower()][0]
    key_date = [field for field in fields if "date" in field.lower()][0]
    for row in reader:
        if row[key_ssi]:
            for key in row.keys():
                if key != key_date:
                    row[key] = float(row[key])
            ssi = row[key_ssi]
            # if ssi < 0:
            #     ssi = -1/ssi
            # ssi = math.log(ssi)
            if ssi < 0:
                ssi += 1
            else:
                ssi -= 1
            ts = time.strptime(row[key_date], "%d/%m/%Y %H:%M:%S")
            bars.add(Bar(
                timestamp=time.mktime(ts),
                open_ask=row[key_open_ask],
                open_bid=row[key_open_bid],
                close_ask=row[key_close_ask],
                close_bid=row[key_close_bid],
                ssi=ssi
            ))
    f.close()
    bars.sort()
    return bars
