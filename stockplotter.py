import plotly.express as px
import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import pandas_datareader.data as web
from datetime import date, timedelta


# NASDAQ 100 tickers
all_tickers = ['AAPL','ADBE','ADI','ADP','ADSK','AEP','ALGN','AMAT',
                'AMD','AMGN','AMZN','ANSS','ASML','ATVI','AVGO','BIDU',
                'BIIB','BKNG','CDNS','CDW','CERN','CHKP','CHTR','CMCSA',
                'COST','CPRT','CRWD','CSCO','CSX','CTAS','CTSH','DLTR',
                'DOCU','DXCM','EA','EBAY','EXC','FAST','FB','FISV','FOX',
                'FOXA','GILD','GOOG','GOOGL','HON','IDXX','ILMN','INCY',
                'INTC','INTU','ISRG','JD','KDP','KHC','KLAC','LRCX','LULU',
                'MAR','MCHP','MDLZ','MELI','MNST','MRNA','MRVL','MSFT',
                'MTCH','MU','NFLX','NTES','NVDA','NXPI','OKTA','ORLY',
                'PAYX','PCAR','PDD','PEP','PTON','PYPL','QCOM','REGN',
                'ROST','SBUX','SGEN','SIRI','SNPS','SPLK','SWKS','TCOM',
                'TEAM','TMUS','TSLA','TXN','VRSK','VRSN','VRTX','WBA',
                'WDAY','XEL','XLNX','ZM']

# Starting graph attributes
start_date = '2020-01-01'
end_date = date.today() - timedelta(days=1)
start_ticker = all_tickers[0]
start_df = web.DataReader(all_tickers[0], 'stooq', start=start_date, end=end_date)
start_trace = go.Scatter(x=start_df.index, y=start_df.Close, mode='lines', name=start_ticker)

# List of dictionaries containing trace dataframe and ticker
stocks = [{
    'ticker': start_ticker,
    'start': start_date,
    'end': end_date,
    'df': start_df
}]


# Create dash board and launch
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Stock Plotter"),
    html.H3('Select symbol from NASDAQ-100'),
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
    html.H4(id='my-output', style={'margin-left': '5%'}),
    dcc.Graph(
        id='stock-graph',
        figure= go.Figure(data=start_trace),
    )
], style={'padding': '3%', 'border': '10px solid grey'})

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
                                     mode='lines', name=stock['ticker']))

    fig = go.Figure(data=traces, 
                    layout=go.Layout(title=f'Closing stock price through interval {pstart} / {pend}'))
    return 'Selected Tickers: {}'.format(tickers), fig


if __name__ == '__main__':
    app.run_server(debug=True)
