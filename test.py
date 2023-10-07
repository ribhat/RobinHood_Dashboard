import requests
import robin_stocks
import robin_stocks.robinhood as robin
import pyotp
from matplotlib import pyplot as plt
import pandas as pd
import datetime

# Dash Imports
from dash import Dash, dcc, Output, Input, html, dash_table  # pip install dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px

plt.style.use('fivethirtyeight')  # use print(plt.style.available) to check out other styles.

month_conversion_dict = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', "June": "06",
                         'July': '07',
                         'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
default_year = 2023

lines = open(
    "C:/Users/bhatr/Desktop/RHCredentials.txt").read().splitlines()  # enter the path to your credentials here or manually enter them on the next line instead of this line
# login = robin.login('bhat.rish@gmail.com', 'Lookatmenow1')

Username = lines[0]
Password = lines[1]

login = robin.login(Username, Password)

my_stocks = robin.build_holdings()
dividend_data = robin.account.get_dividends()


def ViewHoldings():
    """Basic function to view breakdown of all user holdings

        Returns: None"""
    list_of_user_tickers = []
    for key, value in my_stocks.items():
        print(key, value)
        list_of_user_tickers.append(key)
    return list_of_user_tickers


def Quote(ticker):
    """Function used to find a current stock price

        Returns: Float """
    r = robin.get_latest_price(ticker)
    print(ticker.upper(), str(r[0]))
    return float(r[0])


def CreatePieChart():
    """This function creates a pie chart of the users current holdings within Python (not on dashboard)

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


def TotalDividendsYTD(year=default_year):
    """This function will be used to visualize the dividend payouts by each month of the current year in a line graph.
        the x axis will be months and the y axis will be total dividends collected that month.

        Returns: float -> Sum of all dividends collected so far this year
    """

    sum = 0
    dividends_collected = []

    for month in months:
        dividends_collected.append(TotalDivendsPerMonthYTD(month, year))

    # plt.plot(months, dividends_collected, color='#5a7d9a', linestyle='--', marker='o')  # -- means a dashed line
    # plt.title('Dividends Collected by Month')
    # plt.xlabel('Months')
    # plt.ylabel('Dividends Collected')
    # plt.show()

    for item in dividends_collected:
        sum += item

    return float("%.2f" % sum)


def TotalDivendsPerMonthYTD(month, year=default_year):
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
# print(dividend_data[0])
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

## filter dividend_df for results only from 2023 and group them by ticker while summing the amount column
dividend_df['amount'] = dividend_df['amount'].astype(float).round(2)
dividend_this_year_df = dividend_df[dividend_df['payable_date'].str.startswith('2023')]
print(dividend_this_year_df)

amounts_this_year_df = dividend_this_year_df.groupby('Ticker')['amount'].sum().reset_index() # the.reset_index helps us not keep the ticker as our primary key of the df
print("Here is amounts_this_year df: \n")
print(amounts_this_year_df)
print("done")


## filter dividend_df for results only from this year
# print(dividend_df['payable_date'], print(str(default_year)))
# print(type(dividend_df['payable_date']), type(str(default_year)))
#
# dividend_this_year_df = dividend_df.loc[dividend_df['payable_date'] == str(default_year)]
# print("\nThis is the dividend_this_year_df")
# print(dividend_this_year_df.head())
# print(dividend_this_year_df.shape[0])

total_holdings_df = pd.DataFrame(my_stocks.values(), index=my_stocks.keys())
#print(total_holdings_df[0:5])

## Initiate the App

app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

## Build Components

header = dcc.Markdown(children='# Dividend Dashboard')

mygraph = dcc.Graph(figure={})
mypie = dcc.Graph(figure={})

slices = []
labels = []
for ticker, details in my_stocks.items():
    labels.append(ticker)
    slices.append(float(details['equity']))
total_holdings_pie = dcc.Graph(figure=px.pie(names=labels, values=slices, hover_name=labels))
dividendYTD_pie = dcc.Graph(figure=px.pie(names = amounts_this_year_df['Ticker'], values = amounts_this_year_df['amount'], hover_name=amounts_this_year_df['Ticker']))


## Sort DataFrame in Descending order
amounts_this_year_df = amounts_this_year_df.sort_values(by='amount', ascending=False) #sort biggest to smallest
# Define columns list for DataTable. We can use the column list to create the DividendTableYTD
columns_list = []
for col_name in amounts_this_year_df.columns:
    if col_name == "amount":
        column_dict = {
            "name": "Dividends This Year",
            "id": col_name,
            "type": "numeric",
            "format": {"specifier": ".2f"}
        }
    else:
        column_dict = {
            "name": col_name,
            "id": col_name
        }
    columns_list.append(column_dict)
# Define DataTable
DividendTableYTD = dash_table.DataTable(
    id='table',
    columns=columns_list,
    data=amounts_this_year_df.to_dict('records'),
    style_table={'overflowY': 'auto'},
    style_cell={'color': 'blue'}
)

plot_dropdown = dcc.Dropdown(options=['Bar Plot', 'Scatter Plot', 'Line Graph'],
                             value='Bar Plot',  # initial value displayed when page first loads
                             clearable=False)
pie_dropdown = dcc.Dropdown(options=['Total Holdings', 'DividendsYTD'],
                             value='DividendsYTD',  # initial value displayed when page first loads
                             clearable=False)

portfolio_value = dcc.Markdown(children="Portfolio Value: $" + str(robin.profiles.load_portfolio_profile()['equity']))

current_dt = str(datetime.datetime.now())
curr_month = current_dt[5:7]
curr_year = current_dt[0:4]

dividends_this_month = dcc.Markdown(
    children="Dividends this month: $" + str(TotalDivendsPerMonthYTD(str(curr_month), curr_year).round(2)))
dividends_this_year = dcc.Markdown(
    children="Dividends so far this year: $" + str(TotalDividendsYTD(curr_year).round(2)))

## DESIGN APP LAYOUT

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([header], width={"size": 6, "offset": 3})
    ]),
    dbc.Row([
        dbc.Col([mypie], width=6),
        dbc.Col([portfolio_value], width = 1),
        dbc.Col([mygraph], width = 5)
    ]),
    dbc.Row([
        dbc.Col([pie_dropdown], width=6),
        dbc.Col(width=1),
        dbc.Col([plot_dropdown], width=5)      #
    ]),
dbc.Row([
        dbc.Col(),
        dbc.Col(),
        dbc.Col()
    ]),
    dbc.Row([
        dbc.Col(),
        dbc.Col(),
        dbc.Col([dividends_this_month], width=4)
    ]),
    dbc.Row([
        dbc.Col([DividendTableYTD], width=4),
        dbc.Col( width=4),
        dbc.Col([dividends_this_year], width= 4)
    ])

])


## Callback allows components to interact
@app.callback(
    Output(mygraph, component_property='figure'),
    Output(mypie, component_property='figure'),
    Input(plot_dropdown, component_property='value'),
    Input(pie_dropdown, component_property='value')
)
def update_graph(plot_input, pie_input):  ## function arguments come from the component property of the Input
    ## Update the Bar/Scatter/Line Plot
    dividends_collected = []

    for month in months:
        dividends_collected.append(TotalDivendsPerMonthYTD(month, 2023)) #create an array that represents dividends collected each month

    if plot_input == 'Bar Plot':
        plot_fig = px.bar(data_frame=dividend_df, x=months, y=dividends_collected, title='Dividend Breakdown by Month',
                          width=525, height=500)

    elif plot_input == 'Scatter Plot':
        plot_fig = px.scatter(data_frame=dividend_df, x=months, y=dividends_collected, title='Dividend Breakdown by Month',
                              width=525, height=500)

    elif plot_input == 'Line Graph':
        plot_fig = px.line(data_frame=dividend_df, x=months, y=dividends_collected, title='Dividend Breakdown by Month',
                           width=525, height=500)

    ## Update the Pie Chart:
    if pie_input == 'Total Holdings':
        slices = []
        labels = []
        for ticker, details in my_stocks.items():
            labels.append(ticker)
            slices.append(float(details['equity']))
        pie_fig = px.pie(names=labels, values=slices, hover_name=labels, title='Portfolio Breakdown',
                         width=637, height=500, hole=.02)
    else:
        pie_fig = px.pie(data_frame=amounts_this_year_df, names=amounts_this_year_df['Ticker'],
                         values=amounts_this_year_df['amount'], hover_name=amounts_this_year_df['Ticker'],
                         title='Dividends Received TYD', width=635, height=500, hole=.02)

    return plot_fig, pie_fig  # returned objects are assigned to the component property of the Output


app.run_server(port=8053)