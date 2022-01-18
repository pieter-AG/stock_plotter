import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

from pandas_datareader import data as pdr
from datetime import date

# df_nasdaq = pdr.get_nasdaq_symbols()
# tickers = df_nasdaq.loc[:,"NASDAQ Symbol"].tolist()

tickers = ['AAPL', 'AMZN', 'GOOG', 'TSLA']

app = dash.Dash('Stock Plotter')

app.layout = html.Div([
    html.H1("Stock Plotter Dashboard"),
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in tickers],
        value=tickers[0]
    ),
    dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date.today(),
        initial_visible_month=date(2022, 1, 1),
        end_date=date.today()
    ),

], style={'text-align': 'center'})


if __name__ == '__main__':
    app.run_server()


