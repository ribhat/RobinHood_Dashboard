import robin_stocks
import robin_stocks.robinhood as robin
import pyotp
from matplotlib import pyplot as plt

# totp = pyotp.TOTP("My2FactorAppHere").now()
# print("current OTP:", totp)

lines = open("C:/Users/bhatr/Desktop/RHCredentials.txt").read().splitlines() #enter the path to your credentials here or manually enter them on the next line instead of this line
#login = robin.login('bhat.rish@gmail.com', 'Lookatmenow1')

Username = lines[0]
Password = lines[1]

login = robin.login(Username, Password)



my_stocks = robin.build_holdings()


def ViewHoldings():
    for key, value in my_stocks.items():
        print(key, value)


def Quote():
    ticker = input("Enter ticker: ")
    r = robin.get_latest_price(ticker)
    print(ticker.upper(), str(r[0]))


def CreatePieChart():
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


CreatePieChart()
# Quote()
#ViewHoldings()
