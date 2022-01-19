import plotly.express as px
import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import pandas_datareader.data as web
from datetime import date

app = dash.Dash(__name__)
# Fetches all tickers listed on nasdaq
all_tickers = ['AAPL', 'AMZN', 'GOOG', 'TSLA']

# Starting graph attributes
start_ticker = all_tickers[0]
start_df = web.DataReader(all_tickers[0], 'stooq', start='2022-01-01', end='2022-01-18')
start_trace = go.Scatter(x=start_df.index, y=start_df.Close, mode='lines+markers', name=start_ticker)

# List of dictionaries containing trace dataframe and ticker
stocks = [{
    'ticker': start_ticker,
    'df': start_df
}]

app.layout = html.Div([
    html.H1("Select a company's ticker from the dropdown below"),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in all_tickers],
        value=[start_ticker],
        multi=True
    ),
    html.Br(),
    html.Div(id='my-output'),
    dcc.Graph(
        id='stock-graph',

        # Starting trace
        figure= go.Figure(data=start_trace),
    )
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Output('stock-graph', 'figure'),
    Input(component_id='ticker-dropdown', component_property='value')
)
def update_output_div(tickers):
    # Add new dictionary to stocks, if not allready in stocks
    for ticker in tickers:
        if ticker not in [stock['ticker'] for stock in stocks]:
            stocks.append({
                'ticker': ticker,
                'df': web.DataReader(ticker, 'stooq', start='2022-01-01', end='2022-01-18')
            })

    # Create list of traces which will be plotted
    traces = []
    for stock in stocks:
        if stock['ticker'] in tickers:
            traces.append(go.Scatter(x=stock['df'].index, y=stock['df'].Close, mode='lines+markers', name=stock['ticker']))

    fig = go.Figure(data=traces)
    return 'Selected Tickers: {}'.format(tickers), fig


if __name__ == '__main__':
    app.run_server(debug=True)
