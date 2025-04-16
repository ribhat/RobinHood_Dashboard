import requests
import robin_stocks
import robin_stocks.robinhood as robin
import pyotp
from matplotlib import pyplot as plt
import pandas as pd
import datetime
import getpass
import data.api as api
from constants import month_conversion_dict, months, default_year, curr_year, curr_month, curr_day

# Dash Imports
from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px

plt.style.use('fivethirtyeight')  # use print(plt.style.available) to check out other styles.



login = api.login()

print("login successful")



my_stocks = api.get_holdings()
dividend_data = api.get_dividend_data()


def ViewHoldings():
    """Basic function to view breakdown of all user holdings

        Returns: None"""
    for key, value in my_stocks.items():
        print(key, value)



def CreatePieChart():
    """This function creates a pie chart of the users current holdings

        Returns: None"""
    slices = []
    labels = []
    for ticker, details in my_stocks.items():
        labels.append(ticker)
        slices.append(float(details['equity']))

    explode = [.01] * len(slices)

    plt.pie(slices, labels=labels, wedgeprops={'edgecolor': 'black'}, explode=explode,
            autopct='%1.1f%%')

    plt.title("Allocation Breakdown")
    plt.tight_layout()
    plt.show()


def DividendHistory(year=default_year):
    """This function will be used to visualize the dividend payouts by each month of the current year in a line graph.
        the x axis will be months and the y axis will be total dividends collected that month.

        Returns: int -> Sum of all dividends collected so far this year
    """

    sum = 0
    dividends_collected = []

    for month in months:
        dividends_collected.append(TotalDivendsForMonth(month, year))

    # plt.plot(months, dividends_collected, color='#5a7d9a', linestyle='--', marker='o')  # -- means a dashed line
    # plt.title('Dividends Collected by Month')
    # plt.xlabel('Months')
    # plt.ylabel('Dividends Collected')
    # plt.show()

    for item in dividends_collected:
        sum += item

    return float("%.2f" % sum)


def TotalDivendsForMonth(month, year=default_year):
    """Helper function to return total dividends acquired in a particular month
        Inputs:
        month is str of the month name or str of month number
        year is either a str year or int year

        Returns: float"""
    sum = 0
    if len(str(month)) != 2:
        month = month_conversion_dict[month]
    for dictionary in dividend_data:
        if dictionary['payable_date'][0:7] == str(year) + '-' + str(month) and dictionary['state'] != 'voided':
            # print(dictionary)
            # print(float(dictionary['amount']))
            sum += float(dictionary['amount'])
    return float("%.2f" % sum)


# CreatePieChart()
# Quote()
# ViewHoldings()
# print(TotalDivendsForMonth('June', 2023))
# DividendHistory(2023)
print(dividend_data[0])
response = requests.get(dividend_data[0]['instrument'])
#print(response.json())

# --------------------------------------------------------------------------------------------------------------------
### BUILDING A DASHBOARD

dividend_df = pd.DataFrame(dividend_data)
pd.set_option('display.max_columns', None)
#print(dividend_df.head())

## use this code if figure out how to have a diffirent color for each ticker on the bar chart.
## need to compose a list of all the symbols (tickers)

## This code adds the ticker as a column to the dividend_df
tickers = []
for i in range(len(dividend_data)):
    response = requests.get(dividend_data[i]['instrument'])
    tickers.append(response.json()['symbol'])
dividend_df['Ticker'] = tickers

print(dividend_df.head())

print("---------------------------------")


## filter dividend_df for results only from this year
print(dividend_df['payable_date'], str(default_year))
print("-----")
print(type(dividend_df['payable_date']), type(str(default_year)))
print("-----")

dividend_this_year_df = dividend_df.loc[dividend_df['payable_date'] == str(default_year)]
print("\nThis is the dividend_this_year_df")
print(dividend_this_year_df.head())
print(dividend_this_year_df.shape[0])

total_holdings_df = pd.DataFrame(my_stocks.values(), index=my_stocks.keys())
#print(total_holdings_df[0:5])

## Initiate the App

app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

## Build Components

header = dcc.Markdown(children='# Dividend Dashboard')
mygraph = dcc.Graph(figure={})

slices = []
labels = []
for ticker, details in my_stocks.items():
    labels.append(ticker)
    slices.append(float(details['equity']))
mypie = dcc.Graph(figure=px.pie(names=labels, values=slices, hover_name=labels))
dropdown = dcc.Dropdown(options=['Bar Plot', 'Scatter Plot', 'Line Graph'],
                        value='Bar Plot',  # initial value displayed when page first loads
                        clearable=False)

portfolio_value = dcc.Markdown(children="Portfolio Value: $" + str(api.get_portfolio_value()))

dividends_this_month = dcc.Markdown(
    children="Dividends this month: $" + str(TotalDivendsForMonth(str(curr_month), curr_year)))
dividends_this_year = dcc.Markdown(children="Dividends so far this year: $" + str(DividendHistory(curr_year)))

# Design App Layout

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([header], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mypie], width=6), dbc.Col([mygraph], width=6)
    ]),
    dbc.Row([
        dbc.Col(), dbc.Col([dropdown], width=6)
    ], justify='right'),
    dbc.Row([
        dbc.Col([portfolio_value], width=6), dbc.Col([dividends_this_month], width=6)
    ]),
    dbc.Row([
        dbc.Col(), dbc.Col([dividends_this_year], width=6)


    #Include a scrollable table that lists the dividends recieved this year
    ])
])


# Callback allows components to interact
@app.callback(
    Output(mygraph, component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_graph(user_input):  # function arguments come from the component property of the Input
    dividends_collected = []

    for month in months:
        dividends_collected.append(TotalDivendsForMonth(month, default_year)) #create an array that represents dividends collected each month

    if user_input == 'Bar Plot':
        fig = px.bar(data_frame=dividend_df, x=months, y=dividends_collected, title='Dividend Breakdown by Month')

    elif user_input == 'Scatter Plot':
        fig = px.scatter(data_frame=dividend_df, x=months, y=dividends_collected, title='Dividend Breakdown by Month')

    elif user_input == 'Line Graph':
        fig = px.line(data_frame=dividend_df, x=months, y=dividends_collected, title='Dividend Breakdown by Month')

    return fig  # returned objects are assigned to the component property of the Output


app.run(port=8053)
