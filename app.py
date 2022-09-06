from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


df = pd.read_csv("logs/my04_wrx_stock_3rd_1.csv")
df_rpm = df['Engine Speed (rpm)']
df.drop(['Time (msec)','Engine Speed (rpm)'], axis=1, inplace=True)

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(y=df['Throttle Opening Angle (%)'], name="Throttle", line=dict(color='orange')),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(y=df['Mass Airflow (g/s)'], name="Airflow (g/s)", line=dict(color='skyblue')),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(y=df['A/F Sensor #1 (AFR)'], name="AFR", line=dict(color='navy')),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(y=df['Injector Duty Cycle (%)'], name="Inj Duty", line=dict(color='pink')),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(y=df['Manifold Relative Pressure (Corrected) (psi)'], name="Boost", line=dict(color='gold')),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(y=df['Primary Wastegate Duty Cycle (%)'], name="WG Duty", line=dict(color='purple')),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(y=df['Ignition Total Timing (degrees)'], name="Total Ign Timing", line=dict(color='limegreen')),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(y=df['IAM* (raw ecu value)'], name="IAM", line=dict(color='forestgreen')),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(y=df['Feedback Knock Correction* (degrees)'], name="FBKC", line=dict(color='black')),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(y=df['Fine Learning Knock Correction* (degrees)'], name="FLKC", line=dict(color='brown')),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(y=df['Knock Correction Advance (degrees)'], name="Knock Corr Adv", line=dict(color='grey')),
    secondary_y=False
)
### Add Secondary Axis Trace ###
fig.add_trace(
go.Scatter(y=df_rpm, name="RPM", line=dict(color='red')),
secondary_y=True
)

# Format
# Add figure title
fig.update_layout(
title_text="MY 04 WRX Stock 3rd Gear Pull")

fig.update_layout(hovermode="x unified")

fig.layout.yaxis1.update(showticklabels=False)

# Set y-axes title
fig.update_yaxes(title_text="<b>Engine RPM</b>", secondary_y=True)

app.layout = html.Div(children=[
    html.H1(children='RomRaider Log Viewer'),

    html.Div(children='''
        See your log below.
    '''),

    dcc.Graph(id='log',
    figure=fig,
    style={'width': '100vw', 'height': '90vh'})
])

if __name__ == '__main__':
    app.run_server(debug=True)