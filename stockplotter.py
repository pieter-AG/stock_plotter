import plotly.express as px
import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import pandas_datareader.data as web
from datetime import date

# Fetches all tickers listed on nasdaq
all_tickers = ['AAPL', 'AMZN', 'GOOG', 'TSLA']

# Starting graph attributes
start_date = '2022-01-01'
end_date = '2022-01-18'
start_ticker = all_tickers[0]
start_df = web.DataReader(all_tickers[0], 'stooq', start=start_date, end=end_date)
start_trace = go.Scatter(x=start_df.index, y=start_df.Close, mode='lines+markers', name=start_ticker)

# List of dictionaries containing trace dataframe and ticker
stocks = [{
    'ticker': start_ticker,
    'start': start_date,
    'end': end_date,
    'df': start_df
}]

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Select a company's ticker from the dropdown below"),
    html.Div([
        dcc.Dropdown(
            id='ticker-dropdown',
            options=[{'label': ticker, 'value': ticker} for ticker in all_tickers],
            value=[start_ticker],
            multi=True
        ),
    ], style={'width': '40%', 'padding': '0.5%'}),
    html.Div([
        dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=date(2000, 1, 1),
        max_date_allowed=date.today(),
        start_date=start_date,
        end_date=end_date,
        ),
    ], style={'width': '20%', 'padding': '0.5%'}),
    html.Br(),
    html.Div(id='my-output'),
    dcc.Graph(
        id='stock-graph',
        figure= go.Figure(data=start_trace),
    )
], style={'padding': '1%', 'margin': '0 auto'})

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Output('stock-graph', 'figure'),
    Input(component_id='ticker-dropdown', component_property='value'),
    Input(component_id='date-picker-range', component_property='start_date'),
    Input(component_id='date-picker-range', component_property='end_date')
)
def update_output_div(tickers, pstart, pend):
    # Update stocks' dictionaries if start/ end date has changed
    for c, stock in enumerate(stocks[:]):
        if not stock['start'] == pstart or not stock['end'] == pend:
            stocks.pop(c)           # pop and inserting in for-loop is probably not 
            stocks.insert(c, {         # best practice, but anyways...
                'ticker': stock['ticker'],      
                'start': pstart,
                'end': pend,
                'df': web.DataReader(stock['ticker'], 'stooq', start=pstart, end=pend)
            })

    # Add new dictionary to stocks, if not allready in stocks
    tickers_update = []         # List of stocks that require a date-range update
    for ticker in tickers:
        if ticker not in [stock['ticker'] for stock in stocks]:
            stocks.append({
                'ticker': ticker,
                'start': pstart,
                'end': pend,
                'df': web.DataReader(ticker, 'stooq', start=pstart, end=pend)
            })

    # Create list of traces which will be plotted
    traces = []
    for stock in stocks:
        if stock['ticker'] in tickers:
            traces.append(go.Scatter(x=stock['df'].index, y=stock['df'].Close, 
                                     mode='lines+markers', name=stock['ticker']))

    fig = go.Figure(data=traces, 
                    layout=go.Layout(title=f'Stock price through interval {pstart} / {pend}'))
    return 'Selected Tickers: {}'.format(tickers), fig


if __name__ == '__main__':
    app.run_server(debug=True)
