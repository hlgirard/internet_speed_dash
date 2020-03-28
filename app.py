import pandas as pd

# Dash
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

def df():
    path_to_log = '/Users/hlgirard/Downloads/speedlog.csv'
    header = ['Server ID','Sponsor','Server Name','Timestamp','Distance','Ping','Download','Upload','Share','IP Address']
    return pd.read_csv(path_to_log, names=header)

#########################
# Dashboard Layout / View
#########################

# Create the Dash app and get bootstrap CSS
app = dash.Dash()
app.css.append_css({
    "external_url": "bootstrap.min.css"
})

# Main layout
app.layout = html.Div([

    # Title Row
    html.Div(
        [
            html.H1(
                'Internet Speed Monitor',
                style = {'font-family': 'Helvetica',
                       "margin-top": "25",
                       "margin-bottom": "0",
                       "padding-left": 30},
                className = 'col-9',
            ),
            html.P(
                'Displays the historic internet speed.',
                style = 
                    {
                        'font-family': 'Helvetica',
                        "font-size": "120%",
                        "width": "80%",
                        'padding-left': 30,
                    },
                className='col-9',
            )
        ],
        className = 'row'
    ),

    # Update Button
    html.Div(
        [   
            # Dropdown to select saved data to display
            html.Div([
                html.Button(
                    'Update',
                    id = "button-update",
                    style = {'margin': 'auto', 'margin-top': '25'},
                    className = "btn btn-primary"
                )
            ], className = "col-5"),
        ],
        className = 'row'
    ),

    # Graph
    html.Div([

        # Plot Download
        html.Div([
            dcc.Graph(
                id = "plot_download",
                style = {'margin-top': '20'},
                figure = px.scatter(df(), x='Timestamp', y='Download', color='Server Name'),
                animate = True
            )
        ], className = "col-4"),

        # Plot Upload
        html.Div([
            dcc.Graph(
                id = "plot_upload",
                style = {'margin-top': '20'},
                figure = px.scatter(df(), x='Timestamp', y='Upload', color='Server Name'),
                animate = True
            )
        ], className = "col-4"),


        ], className = "col-8"),

    dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds
        n_intervals=0
        )

], className = '.container')

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