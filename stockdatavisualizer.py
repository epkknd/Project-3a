import requests
import matplotlib.pyplot as plt, mpld3
import matplotlib.dates as mdates
from datetime import datetime

def AV_Query(symbol, function):
    apikey = "T6IGSBW0GEMTVTMA"
    if function == "TIME_SERIES_INTRADAY":
        url = 'https://www.alphavantage.co/query?interval=60min&function=' + function + '&symbol=' + symbol + '&apikey=' + apikey 
    else:
        url = 'https://www.alphavantage.co/query?&function=' + function + '&symbol=' + symbol + '&apikey=' + apikey 
    r = requests.get(url)
    data = r.json()
    return data

def menu():
    while True:
        stocksymbol = input("Enter the stock symbol: ")
        if len(stocksymbol) not in range(1,8) or not stocksymbol.isupper() or not stocksymbol.isalpha():
            print("Input must 1-7 capitalized alphabetic characters.")
        if not AV_Query(stocksymbol,"TIME_SERIES_MONTHLY").get("Error Message"):
            break
        else:
            print(stocksymbol, "does not exist.")
    print()
    choice = 0
    while True: 
        print("Time Series Function")
        print("1. Weekly")
        print("2. Monthly") 
        
        try:     
            choice = int(input("Select a time series function: (1-2) "))
            if choice < 1 or choice > 2:
                raise ValueError
        except ValueError:
            print("Input must be an int between 1-2.")
        else:
            break
    function = ""
    if choice == 1:
        function = "TIME_SERIES_WEEKLY"
    elif choice == 2:
        function = "TIME_SERIES_MONTHLY"
    print()
    while True:
        try:
            startdate = datetime.strptime(input("Enter the beginning date in YYYY-MM-DD format: "), '%Y-%m-%d' )
            enddate = datetime.strptime(input("Enter the end date in YYYY-MM-DD format: "), '%Y-%m-%d')
            if startdate > enddate:
                raise ValueError("Start date is after end date.")
        except ValueError as e:
            print(e)
        else:
            break
    return (stocksymbol, function, startdate, enddate)
        
def graphData(data, function, startdate, enddate):
    opening_prices = list()
    high_prices = list()
    low_prices = list()
    closing_prices = list()
    
    if function == "TIME_SERIES_WEEKLY":
        function = "Weekly Time Series"
    elif function == "TIME_SERIES_MONTHLY":
        function = "Monthly Time Series"    
    values = data.get(function).values()
    for datapoint in values:
        opening_prices.append(datapoint.get("1. open"))
        high_prices.append(datapoint.get("2. high"))
        low_prices.append(datapoint.get("3. low"))
        closing_prices.append(datapoint.get("4. close"))
    
    
    
    datestrings = list(data.get(function).keys())
    dates = list()
    for d in datestrings:
        dates.append(datetime.strptime(d, '%Y-%m-%d'))
        
    x_values  = mdates.date2num(dates)
    
    fig, ax = plt.subplots(figsize=(10,10))
    
    ax.plot(x_values, opening_prices, '-o', label="Open")
    ax.plot(x_values, high_prices, '-o', label="High")
    ax.plot(x_values, low_prices, '-o', label="Low")
    ax.plot(x_values, closing_prices, '-o', label="Closing")
    ax.legend()
    ax.set_title(function)
    
    locator = mdates.AutoDateLocator(minticks=5, maxticks=12)
    date_formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis_date()
    ax.set_xlim(mdates.date2num(startdate), mdates.date2num(enddate))
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(date_formatter)
    
    mpld3.fig_to_html(fig)
    mpld3.show()
 
    
def main():
    choices = menu()
    data = AV_Query(choices[0], choices[1])
    graphData(data, choices[1], choices[2], choices[3])
  
main()

    