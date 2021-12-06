import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import requests
import json

# Initialize the app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
apikey = '88BF8257-E755-46D1-B79B-231FA32B11C9'
app.title = 'Africa Data School Crypto App'
app.description = "This is a test app for Africa Data School August 2021 Cohort"
app.layout = html.Div(children=[
    html.Link(rel='shortcut icon', type='favicon.ico', href='assets/btc.png'),
    html.Div([
        html.Div([
            # image
            html.Img(src=app.get_asset_url('btc.png'), id='ads-image', style={
                'height': '60px',
                'width': 'auto',
                'margin-bottom': '25px'
            })
        ], className='one-third column'),
        # Adds heading   DIV
        html.Div([
            # heading
            html.Div([
                html.H3('Africa Data School ', style={'margin-bottom': '5px', 'color': 'purple', 'font-weight': 'bold'}),
                html.H5('Cryptocurrency Prices', style={'margin-bottom': '0px', 'color': 'purple'})
            ])

        ], className='one-third column', id='title'),
    ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),
    # DROPDOWN SECTION

    html.Div([
        # Select crypto
        html.Div([
            html.Label('Crypto Asset', style={'color': '#FF00BD'}),
            dcc.Dropdown(
                id='coin',
                options=[
                    {'label': 'Bitcoin', 'value': 'BTC'},
                    {'label': 'Ethereum', 'value': 'ETH'},
                    {'label': 'Bitcoin Cash', 'value': 'BCH'},
                    {'label': 'Litecoin', 'value': 'LTC'}
                ],
                value='BTC'
            ),

        ], className='card_container three columns'),

        # Select Time Period
        html.Div([
            html.Label('Time', style={'color': '#FF00BD'}),
            dcc.Dropdown(
                id='time',
                options=[
                    {'label': 'Minute', 'value': '1MIN'},
                    {'label': 'Day', 'value': '10DAY'},
                    {'label': 'Month', 'value': '3MTH'},
                    {'label': 'year', 'value': '1YRS'}
                ],
                value='10DAY'
            ),

            dcc.Interval(
                id='graph-update',
                interval=1 * 10,
                n_intervals=0
            ),

        ], className='card_container three columns'),
    ], className='row flex display'),

    html.Div([
        # Price Opening
        html.Div([
            html.H6(children='Price Open',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(id='price_open',
                   style={'textAlign': 'center',
                          'color': 'orange',
                          'fontSize': 40}),

        ], className='card_container three columns'),
        # Price Closing
        html.Div([
            html.H6(children='Price Close',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(id='price_close',
                   style={'textAlign': 'center',
                          'color': 'orange',
                          'fontSize': 40}),

        ], className='card_container three columns'),
        # Price high
        html.Div([
            html.H6(children='Price High',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(id='price_high',
                   style={'textAlign': 'center',
                          'color': 'orange',
                          'fontSize': 40}),

        ], className='card_container three columns'),
        # Volume Traded
        html.Div([
            html.H6(children='Volume Traded',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(id='Volume_traded',
                   style={'textAlign': 'center',
                          'color': 'orange',
                          'fontSize': 40}),

        ], className='card_container three columns')
    ], className='row flex display'),
    # THE GRAPH
    html.Div([
        html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': False}),
        ], className='card_container twelve columns')
    ], className='row flex display'),
], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

# APPLY CALLBACKS to LINK the APP FUNCTIONALITY TO THE APP LAYOUT
@app.callback(
    [
        Output(component_id='price_open', component_property='children'),
        Output(component_id='price_close', component_property='children'),
        Output(component_id='price_high', component_property='children'),
        Output(component_id='Volume_traded', component_property='children'),
        Output(component_id='graph', component_property='figure')
    ],
    [
        Input(component_id='coin', component_property='value'),
        Input(component_id='time', component_property='value')
    ]
)
def update_content(currency, time_change):
    """This Function fetches the data from Coin API and returns the price_close,
    price_high, price_open, volume traded and the graph.
    """
    url = f'https://rest.coinapi.io/v1/ohlcv/{currency}/USD/latest?period_id={time_change}'
    headers = {'X-CoinAPI-Key': apikey}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    df = pd.DataFrame(data)
    # Price Open
    price_open = df['price_open'][0]
    # Price Close
    price_close = df['price_close'][0]
    # Price High
    price_high = df['price_high'][0]
    # Volume
    volume_traded = round(df['volume_traded'][0], 2)
    fig = go.Figure(data=[go.Candlestick(x=df.time_period_start,
                                         open=df.price_open,
                                         high=df.price_high,
                                         low=df.price_low,
                                         close=df.price_close,
                                         text=currency)],
                    )

    fig.update_layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                      template='plotly_dark',
                      paper_bgcolor='rgba(0, 0, 0, 0)',
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      margin={'b': 15},
                      hovermode='x',
                      autosize=True,
                      title={'text': f'Cryptocurrency Prices for {currency} ', 'font': {'color': 'white'}, 'x': 0.5}, )

    return price_open, price_close, price_high, volume_traded, fig


if __name__ == "__main__":
    app.run_server(debug=True)
