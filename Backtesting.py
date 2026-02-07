import pandas as pd
import numpy as np
import vectorbt as vbt
from datetime import datetime
import talib

data = pd.read_csv(
    "Bitstamp__BTCUSD_1h.csv",
    skiprows=1  
)

data.columns = [c.lower() for c in data.columns]

data["unix"] = pd.to_datetime(data["unix"], unit="s")
data.set_index("unix", inplace=True)

data = data.sort_index()

ohlc = data[["open", "high", "low", "close"]].astype(float)

open_  = np.ascontiguousarray(ohlc["open"].values, dtype=np.double)
high_  = np.ascontiguousarray(ohlc["high"].values, dtype=np.double)
low_   = np.ascontiguousarray(ohlc["low"].values, dtype=np.double)
close_ = np.ascontiguousarray(ohlc["close"].values, dtype=np.double)

hammer = talib.CDLHAMMER(open_, high_, low_, close_)
hanging_man = talib.CDLHANGINGMAN(open_, high_, low_, close_)

buy = hammer == 100
sell = hanging_man == -100

pf = vbt.Portfolio.from_signals(
    ohlc["close"],
    buy,
    sell,
    #fee=0.005
)

print(pf.stats())
pf.plot().show()
