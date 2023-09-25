import robin_stocks
import robin_stocks.robinhood as robin
import pyotp
from matplotlib import pyplot as plt
import pandas as pd
import datetime

# Dash Imports
from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px

plt.style.use('fivethirtyeight')  # use print(plt.style.available) to check out other styles.

month_conversion_dict = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', "June": "06",
                         'July': '07',
                         'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']

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
    for key, value in my_stocks.items():
        print(key, value)



def Quote(ticker):
    """Function used to find a current stock price

        Returns: Float """
    r = robin.get_latest_price(ticker)
    print(ticker.upper(), str(r[0]))
    return float(r[0])


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


def DividendHistory(year):
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


def TotalDivendsForMonth(month, year):
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



# BUILDING A DASHBOARD ------------------------------------------------------------------------------------------

# dividend_df = pd.DataFrame(dividend_data)
# print(dividend_df[0:5])
# df = pd.DataFrame(my_stocks.values(), index=my_stocks.keys())
# print(df[0:5])
#
#
# #Initiate the App
#
# app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
#
# #Build Components
#
# header = dcc.Markdown(children='# Portfolio Dashboard')
# mygraph = dcc.Graph(figure={})
#
# slices = []
# labels = []
# for ticker, details in my_stocks.items():
#     labels.append(ticker)
#     slices.append(float(details['equity']))
# mypie = dcc.Graph(figure=px.pie(names=labels, values=slices, hover_name=labels))
# dropdown = dcc.Dropdown(options=['Bar Plot', 'Scatter Plot', 'Line Graph'],
#                         value='Bar Plot',  # initial value displayed when page first loads
#                         clearable=False)
#
# portfolio_value = dcc.Markdown(children="Portfolio Value: $" + str(robin.profiles.load_portfolio_profile()['equity']))
#
# current_dt = str(datetime.datetime.now())
# curr_month = current_dt[5:7]
# curr_year = current_dt[0:4]
# dividends_this_month = dcc.Markdown(children="Dividends this month: $" + str(TotalDivendsForMonth(str(curr_month), curr_year)))
# dividends_this_year = dcc.Markdown(children="Dividends so far this year: $" + str(DividendHistory(curr_year)))
#
# #Design App Layout
#
# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([header], width = 6)
#     ], justify='center'),
#     dbc.Row([
#         dbc.Col([mypie], width = 6), dbc.Col([mygraph], width = 6)
#     ]),
#     dbc.Row([
#         dbc.Col(), dbc.Col([dropdown], width = 6)
#     ], justify='right'),
#     dbc.Row([
#         dbc.Col([portfolio_value], width=6), dbc.Col([dividends_this_month], width = 6)
#     ]),
#     dbc.Row([
#         dbc.Col(), dbc.Col([dividends_this_year], width = 6)
#     ])
# ])
#
# # Callback allows components to interact
# @app.callback(
#     Output(mygraph, component_property='figure'),
#     Input(dropdown, component_property='value')
# )
# def update_graph(user_input):  # function arguments come from the component property of the Input
#     dividends_collected = []
#
#     for month in months:
#         dividends_collected.append(TotalDivendsForMonth(month, 2023))
#
#     if user_input == 'Bar Plot':
#         fig = px.bar(data_frame=dividend_df, x=months, y=dividends_collected, title = 'Dividend Breakdown by Month')
#
#     elif user_input == 'Scatter Plot':
#         fig = px.scatter(data_frame=dividend_df, x=months, y=dividends_collected, title = 'Dividend Breakdown by Month')
#
#     elif user_input == 'Line Graph':
#         fig = px.line(data_frame=dividend_df, x=months, y=dividends_collected, title = 'Dividend Breakdown by Month')
#
#     return fig  # returned objects are assigned to the component property of the Output
#
# app.run_server(port=8053)