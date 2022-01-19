import plotly.express as px
import plotly.graph_objects as go

import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

import pandas_datareader.data as web
from datetime import date

app = dash.Dash(__name__)
tickers = ['AAPL', 'AMZN', 'GOOG', 'TSLA']
df = [web.DataReader(tickers[0], 'stooq', start='2022-01-01', end='2022-01-18')]
prev = []

app.layout = html.Div([
    html.H1("Select a company's ticker from the dropdown below"),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in tickers],
        value=[tickers[0]],
        multi=True
    ),
    html.Br(),
    html.Div(id='my-output'),
    dcc.Graph(
        id='stock-graph',
        figure= go.Figure(data=go.Scatter(x=df[0].index, y=df[0].Close, mode='markers')),
    )
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Output('stock-graph', 'figure'),
    Input(component_id='ticker-dropdown', component_property='value')
)
def update_output_div(ptickers):
    df_list = []
    traces = []
    for c, pticker in enumerate(ptickers):
        print(f'Current pticker: {pticker}')
        print(f'Current c counter: {c}')
        df_list.append(web.DataReader(pticker, 'stooq', start='2022-01-01', end='2022-01-18'))
        print(df_list[c])
        traces.append(go.Scatter(x=df_list[c].index, y=df_list[c].Close, mode='markers'))
    
    fig = go.Figure(data=traces)
    return 'Selected Tickers: {}'.format(ptickers), fig


if __name__ == '__main__':
    app.run_server(debug=True)
