import base64
import io
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import dash
from dash.dependencies import Input, Output, State
from dash import html, dash_table, dcc

import pandas as pd

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Click here to upload CSV file."]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=False,
        ),
        html.Div(["RomRaider log viewer"]),
        dcc.Graph(id="Mygraph",
        style={'width': '100vw', 'height': '90vh'})
        # html.Div(id="output-data-upload")
    ])

@app.callback(
    Output("Mygraph", "figure"),
    Input("upload-data", "contents"),
)
def update_graph(contents):

    if contents:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        df_rpm = df['Engine Speed (rpm)']
        df.drop(['Time (msec)','Engine Speed (rpm)'], axis=1, inplace=True)
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
        fig.update_layout(hovermode="x unified")

        fig.layout.yaxis1.update(showticklabels=False)

        # Set y-axes title
        fig.update_yaxes(title_text="<b>Engine RPM</b>", secondary_y=True)

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)