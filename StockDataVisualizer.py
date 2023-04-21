import requests
import matplotlib.pyplot as plt, mpld3
import matplotlib.dates as mdates
from datetime import datetime

# I think  I need to turn this into an instancible class to make sure data is being passed between the methods.
class StockDataVisualizer:
    def __init__(self, symbol: str, chart:str, timeseries: str, startdate: datetime, enddate: datetime):
        self.__symbol = symbol
        self.__chart = chart
        self.__timeseries = timeseries
        self.__startdate : datetime = startdate
        print(startdate)
        self.__enddate: datetime  = enddate
        # AV_Query() sets value of self.__data
        self.__AV_Query()
        
    def __AV_Query(self):
        apikey = "T6IGSBW0GEMTVTMA"
        if self.__timeseries == "TIME_SERIES_INTRADAY":
            url = 'https://www.alphavantage.co/query?interval=60min&function=' + self.__timeseries + '&symbol=' + self.__symbol + '&apikey=' + apikey 
        else:
            url = 'https://www.alphavantage.co/query?&function=' + self.__timeseries + '&symbol=' + self.__symbol + '&apikey=' + apikey 
        r = requests.get(url)
        self.__data = r.json()
    
    def graphData(self):
        opening_prices = list()
        high_prices = list()
        low_prices = list()
        closing_prices = list()
        
        if self.__timeseries == "TIME_SERIES_WEEKLY":
            timeseries = "Weekly Time Series"
        elif self.__timeseries == "TIME_SERIES_MONTHLY":
            timeseries = "Monthly Time Series"
        values = self.__data.get(timeseries).values()
        for datapoint in values:
            opening_prices.append(datapoint.get("1. open"))
            high_prices.append(datapoint.get("2. high"))
            low_prices.append(datapoint.get("3. low"))
            closing_prices.append(datapoint.get("4. close"))
        
        datestrings = list(self.__data.get(timeseries).keys())
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
        ax.set_title(self.__timeseries)
        
        locator = mdates.AutoDateLocator(minticks=5, maxticks=12)
        date_formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis_date()
        ax.set_xlim(mdates.date2num(self.__startdate), mdates.date2num(self.__enddate))
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(date_formatter)
        
        return fig
        


        
    def get_data(self):
        return self.__data