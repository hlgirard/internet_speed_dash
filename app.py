import os
import pandas as pd

# Dash
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

PATH_TO_SPEEDTEST_LOG = os.environ.get('PATH_TO_SPEEDTEST_LOG') or '/home/osmc/speedlog.csv'

def df():
    header = ['Server ID','Sponsor','Server Name','Timestamp','Distance','Ping','Download','Upload','Share','IP Address']
    return pd.read_csv(PATH_TO_SPEEDTEST_LOG, names=header)

#########################
# Dashboard Layout / View
#########################

# Create the Dash app and get bootstrap CSS
app = dash.Dash()

# Main layout
app.layout = html.Div([

    # Title Row
    html.Div(
        [
            html.H1(
                'Internet Speed Monitor',
                style = {'font-family': 'Helvetica',
                       "margin-top": "50",
                       "margin-bottom": "0",
                       "padding-left": 30},
            )
        ],
        className = 'row justify-content-center mt-3'
    ),

    # Update Button
    html.Div(
        [   
            # Dropdown to select saved data to display
            html.Div([
                html.Button(
                    'Update',
                    id = "button-update",
                    style = {'margin': 'auto', 'margin-top': '50', 'margin-bottom': '50'},
                    className = "btn btn-primary"
                )
            ]),
        ],
        className = 'row justify-content-center mt-3 mb-3'
    ),

    # Plot Download
    html.Div([
        dcc.Graph(
            id = "plot_download",
            style = {'margin-top': '20'},
            figure = px.scatter(df(), x='Timestamp', y='Download', color='Server Name'),
            animate = True
        )
    ], className = "row justify-content-center"),

    # Plot Upload
    html.Div([
        dcc.Graph(
            id = "plot_upload",
            style = {'margin-top': '20'},
            figure = px.scatter(df(), x='Timestamp', y='Upload', color='Server Name'),
            animate = True
        )
    ], className = "row justify-content-center"),


    dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds
        n_intervals=0
        )

], className = '.container col-xl')

##### Graph Update #####

# Update the graph
@app.callback(
    Output('plot_upload', 'figure'),
    [
        Input('button-update', 'n_clicks'),
        Input('interval-component', 'n_intervals')
    ]
)
def display_plot(n_clicks, n_intervals):
    return px.scatter(df(), x='Timestamp', y='Upload', color='Server Name')

# Update the graph
@app.callback(
    Output('plot_download', 'figure'),
    [
        Input('button-update', 'n_clicks'),
        Input('interval-component', 'n_intervals')
    ]
)
def display_plot(n_clicks, n_intervals):
    return px.scatter(df(), x='Timestamp', y='Download', color='Server Name')

# start Flask server
if __name__ == '__main__':

    app.run_server(
        debug=True,
        host='0.0.0.0',
        port=8050
)