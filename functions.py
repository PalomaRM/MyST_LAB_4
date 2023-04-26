import pandas as pd
import numpy as np

def effectivespread(data):
    df = pd.DataFrame(columns=['timestamp','Close','Spread','Effective Spread'])
    df['timestamp'] = pd.to_datetime(data['datetime'])
    df['Close'] = data['mid_price']
    df['Spread'] = data['spread']
    for i in range(len(df)-5):
        df.loc[i+5,'Effective Spread'] = 2*np.sqrt(np.abs(np.cov(np.diff(df.loc[0:i+5,'Close']))))
    return df.iloc[62:]
