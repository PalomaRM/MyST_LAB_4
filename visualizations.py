import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

btc=pd.read_csv("files/BTCUSDT.csv")
eth=pd.read_csv("files/ETHUSDT.csv")

exchanges = btc["exchange"].unique().tolist()

fig = go.Figure()
for exchange in exchanges:
    exchange_df = btc[btc["exchange"] == exchange]
    fig.add_trace(go.Scatter(x=exchange_df["datetime"], y=exchange_df["mid_price"], name=exchange))

fig.update_layout(title=f"BTC/EUR Mid Price for all Exchanges", xaxis_title="Datetime", yaxis_title="Mid Price")
fig.show()