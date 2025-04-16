import robin_stocks.robinhood as robin
import requests

lines = open("C:/Users/rishs/OneDrive/Desktop/RHCredentials.txt").read().splitlines()  # enter the path to your credentials here or manually enter them on the next line instead of this line

Username = lines[0]
Password = lines[1]

def login():
    login = robin.login(Username, Password)

def get_holdings():
    return robin.build_holdings()

def get_dividend_data():
    return robin.account.get_dividends()

def get_portfolio_value():
    return robin.profiles.load_portfolio_profile()['equity']

def Quote(ticker):
    """Function used to find a current stock price

        Returns: Float """
    r = robin.get_latest_price(ticker)
    print(ticker.upper(), str(r[0]))
    return float(r[0])