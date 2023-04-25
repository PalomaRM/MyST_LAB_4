import data as dt
import functions as fn
import pandas as pd

btc=pd.read_csv("files/BTCUSDT.csv", usecols=['exchange','datetime','levels','ask_size',
                                                'bid_size','mid_price','vwap'])
eth=pd.read_csv("files/ETHUSDT.csv", usecols=['exchange','datetime','levels','ask_size',
                                                'bid_size','mid_price','vwap'])

