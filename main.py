import robin_stocks
import robin_stocks.robinhood as robin
import pyotp
from matplotlib import pyplot as plt

plt.style.use('fivethirtyeight') #use print(plt.style.available) to check out other styles.

month_conversion_dict = {'January': '01', 'February': '02', 'March' : '03', 'April': '04', 'May' : '05', "June" : "06", 'July': '07',
                         'August': '08', 'September': '09', 'October' : '10', 'November':'11', 'December':'12'}
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November' , 'December']


# totp = pyotp.TOTP("My2FactorAppHere").now()
# print("current OTP:", totp)

lines = open("C:/Users/bhatr/Desktop/RHCredentials.txt").read().splitlines() #enter the path to your credentials here or manually enter them on the next line instead of this line
#login = robin.login('bhat.rish@gmail.com', 'Lookatmenow1')

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

    plt.pie(slices, labels=labels, wedgeprops={'edgecolor': 'black'}, explode = explode,
            autopct='%1.1f%%')

    plt.title("Allocation Breakdown")
    plt.tight_layout()
    plt.show()

def DividendHistory(year):
    """This function will be used to visualize the dividend payouts by each month of the current year in a line graph.
        the x axis will be months and the y axis will be total dividends collected that month.

        Returns:None
    """

    dividends_collected = []

    print(type(months), months)
    for month in months:
        dividends_collected.append(TotalDivendsForMonth(month, year))


    print(type(dividends_collected), dividends_collected)
    plt.plot(months, dividends_collected, color = '#5a7d9a', linestyle = '--', marker = 'o') #-- means a dashed line
    plt.title('Dividends Collected by Month')
    plt.xlabel('Months')
    plt.ylabel('Dividends Collected')
    plt.show()


def TotalDivendsForMonth(month, year):
    """Helper function to return total dividends acquired in a particular month

        Returns: float"""
    sum = 0
    month_number = month_conversion_dict[month]
    for dictionary in dividend_data:
        if dictionary['payable_date'][0:7] == str(year) + '-' + month_number and dictionary['state'] != 'voided':
            #print(dictionary)
            #print(float(dictionary['amount']))
            sum += float(dictionary['amount'])
    return float("%.2f" % sum)


#CreatePieChart()
# Quote()
#ViewHoldings()
#print(TotalDivendsForMonth('June', 2023))
DividendHistory(2023)

#up next try to find out how to build a dashboard the charts can be deployed to.