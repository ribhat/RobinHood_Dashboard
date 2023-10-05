# Portfolio Dashboard

A comprehensive web dashboard built to visualize and analyze an investment portfolio, leveraging data from Robinhood and presenting insights using Dash and Plotly.

## 🌟 Features
* **Portfolio Allocation Pie Chart**: Get a quick snapshot of the distribution of your investments across various assets.
* **Dividend Analysis**:
  * **Stacked Bar Chart**: Visualize monthly dividends with a breakdown showing contributions from each stock.
  * **Scatter Plot**: Observe total dividends received each month.
  * **Line Graph**: Track the trend of total dividends over time.
* **Interactive Elements**: Switch between different visual representations (Bar, Scatter, Line) for dividend analysis.
* **Portfolio & Dividend Metrics**: Quick metrics showing current portfolio value and dividends received for the current month/year.
## 🛠️ Tech Stack
* **Backend:**

  * **robin_stocks**: Fetch and process portfolio data from Robinhood.
  * **pandas**: Data manipulation and analysis.
* **Frontend**:

  * **Dash**: Create the web application layout and interactive elements.
  * **Plotly**: Data visualization.
  * **dash_bootstrap_components**: Styling components with Bootstrap.
## 🚀 Getting Started
**Prerequisites**
1. Python 3.x
2. Pip
3. Robinhood Account
   
**Setup**
1. Clone the repository:
   
`print("git clone <repository_url>")`

2. Navigate to the project directory and install the required Python packages:
   
`print("pip install -r requirements.txt")`

3. Save your Robinhood credentials in RHCredentials.txt or directly in the code (not recommended for security reasons).

## Running the App
1. In the terminal, navigate to the project directory.

2. Run the application:

`print("python <main>.py")`

3. Open a web browser and navigate to http://127.0.0.1:8053/ to access the dashboard.

## 🌱 Future Enhancements
* Add more metrics like performance comparison to benchmark indices.
* Implement security features for safer login.
* Extend to support multiple brokerage accounts.
## 🤝 Contributing
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.
