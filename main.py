import data as dt
import functions as fn
import pandas as pd

btc=pd.read_csv("files/BTCUSDT.csv", usecols=['exchange','datetime','levels','ask_size',
                                                'bid_size','spread','mid_price','vwap'])
eth=pd.read_csv("files/ETHUSDT.csv", usecols=['exchange','datetime','levels','ask_size',
                                                'bid_size','spread','mid_price','vwap'])

df_btc = fn.effectivespread(btc)
df_eth = fn.effectivespread(eth)
print(df_eth)