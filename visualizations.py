import plotly.graph_objects as go
import pandas as pd

def visualize_data(df, column_name):
    exchanges = df["exchange"].unique().tolist()

    fig = go.Figure(layout=dict(title=dict(text=f"{column_name.capitalize()}")))

    for exchange in exchanges:
        exchange_df = df[df["exchange"] == exchange].copy()  # Make a copy of the slice
        exchange_df["datetime"] = pd.to_datetime(exchange_df["datetime"])  # Convert datetime column to datetime type
        fig.add_trace(go.Scatter(x=exchange_df["datetime"], y=exchange_df[column_name], name=exchange))
    fig.update_xaxes(title_text="Datetime", title_standoff=25)
    fig.update_yaxes(title_text=column_name.capitalize(), title_standoff=25)

    for i, exchange in enumerate(exchanges):
        fig.add_annotation(dict(text=exchange, xref="paper", yref="paper", x=0.05, y=1.1-(i*0.1), showarrow=False))

    fig.show()
