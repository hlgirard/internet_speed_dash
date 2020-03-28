import csv
import os

# Dash
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

PATH_TO_SPEEDTEST_LOG = os.environ.get('PATH_TO_SPEEDTEST_LOG') or '/home/osmc/speedlog.csv'

def data():
    timestamp = []
    upload = []
    download = []

    with open(PATH_TO_SPEEDTEST_LOG, 'r') as logfile:
        csv_reader = csv.DictReader(logfile)
        for row in csv_reader:
            timestamp.append(row['Timestamp'])
            upload.append(row['Upload'])
            download.append(row['Download'])

    return timestamp, upload, download

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
            figure = go.Figure(go.Scatter(x=[0], y=[0])),
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
    Output('plot_download', 'figure'),
    [
        Input('button-update', 'n_clicks'),
        Input('interval-component', 'n_intervals')
    ]
)
def display_plot(n_clicks, n_intervals):
    timestamp, upload, download = data()
    plotting_data = [
    go.Scatter(x=timestamp, y=upload, name='Upload', mode='markers'),
    go.Scatter(x=timestamp, y=download, name='Download', mode='markers')
    ]

    return go.Figure(plotting_data)

# start Flask server
if __name__ == '__main__':

    app.run_server(
        debug=True,
        host='0.0.0.0',
        port=8050
)