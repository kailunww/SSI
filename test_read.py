import matplotlib.pyplot as plt
import numpy as np
from read import parse_csv
from datetime import datetime

# bars = parse_csv("data\AUDUSD_D1_HistoricalSSI.csv")
# bars = parse_csv("data\AUDUSD_H4_HistoricalSSI.csv")
bars = parse_csv("data\AUDUSD_H1_HistoricalSSI.csv")
t = [datetime.fromtimestamp(bar.timestamp) for bar in bars.bars]
s = [bar.ssi for bar in bars.bars]

plt.plot(t, s)

plt.xlabel('time (s)')
plt.ylabel('voltage (mV)')
plt.title('About as simple as it gets, folks')
plt.grid(True)
plt.savefig("test.png")
plt.show()
