import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import plotly
import plotly.graph_objs as go
from plotly import tools
import seaborn as sns
import matplotlib.pyplot as plt



# Customize Graph Options
sns.set_style({"axes.facecolor": "1.0", 
               "axes.edgecolor": "0.85",
               'axes.grid': True, "grid.color": "0.85",
               "grid.linestyle": "-",
               'axes.labelcolor': '0.4', 
               "xtick.color": "0.4",
               'ytick.color': '0.4'})

flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
sns.set_palette(flatui)

# Current Date
today = datetime.date.today().strftime('%Y-%m-%d')

def stock_df(tickers, start_date, interval, end_date=None):
    if end_date == None:
        end_date = today
        
    return yf.download(tickers,
                          start = start_date,
                          end = end_date,
                          interval = interval)


def plot_prices(stock_DataFrame, name = None, interactive = None):
    # Stock Data
    dates = list(stock_DataFrame.index)
    adj_close = list(stock_DataFrame['Adj Close'])
    Open = list(stock_DataFrame['Open'])
    close = list(stock_DataFrame['Close'])
    high = list(stock_DataFrame['High'])
    low = list(stock_DataFrame['Low'])
    volume = list(stock_DataFrame['Volume'])

    # Create Interactive plot if user specifies 'interactive = True'
    if interactive == True:
        # Create subplots, one to visualize stock prices,
        #   and the other to visualize volume 
        fig = tools.make_subplots(rows=2, cols=1,
                                  subplot_titles=('Stock Prices', 'Volume'),
                                  shared_xaxes=True,
                                  print_grid=False);
                        
        # Stock Prices subplot
        fig.add_trace(
            go.Scatter(x=dates, y=adj_close,
                       mode='lines+markers', name = 'Adj Close'),
            row=1, col=1)
        
        
        fig.add_trace(
            go.Scatter(x=dates, y=Open,
                       mode='lines+markers',name = 'Open'),
            row=1, col=1)
        
        fig.add_trace(
            go.Scatter(x=dates, y=close,
                       mode='lines+markers',name = 'Close'),
            row=1, col=1)
        
        fig.add_trace(
            go.Scatter(x=dates, y=high,
                       mode='lines+markers',name = 'High'),
            row=1, col=1)
        
        fig.add_trace(
            go.Scatter(x=dates, y=low,
                       mode='lines+markers',name = 'Low'),
            row=1, col=1)

        # Volume subplot
        fig.add_trace(
            go.Scatter(x=dates, y=volume,
                       mode='lines+markers',name = 'Volume'),
            row=2, col=1)
        if name != None:
            fig.layout.title = name
        
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Price ($)')
        fig.layout.template = 'plotly_dark'
        plotly.offline.plot(fig)
                
    else:
        #  Plot Prices and Volume using matplotlib
        f, ax = plt.subplots(figsize=(15, 12), nrows = 2, ncols = 1)
        
        stock_DataFrame.iloc[:, 0:5].plot(fontsize = 14,
                          rot = 45,
                          ax = ax[0])
        
        ax[0].set_xlabel("Date", fontsize = 18)
        ax[0].set_ylabel("Price ($)", fontsize = 18)
        
        
        stock_DataFrame.iloc[:, 5].plot(fontsize = 14,
                          rot = 45,
                          ax = ax[1])

        # Add x and y label
        ax[1].set_xlabel("Date", fontsize = 18)
        ax[1].set_ylabel("Price ($)", fontsize = 18)
        
        # Tight layout
        plt.tight_layout()

def plot_candlestick(stock_DataFrame, name = None):
    data=[go.Candlestick(x=stock_DataFrame.index,
                open=stock_DataFrame['Open'],
                high=stock_DataFrame['High'],
                low=stock_DataFrame['Low'],
                close=stock_DataFrame['Close'])]
    
    layout = go.Layout(title = name ,
                       xaxis = dict(title='Date'),
                       yaxis=dict(title = 'Price'),
                       template = 'plotly_dark')
    fig = go.Figure(data = data, layout = layout)
    plotly.offline.plot(fig)


def volatility(stock_DataFrame):
    
    closing_prices = list(stock_DataFrame['Close'])
    mean = np.mean(closing_prices)
    
    diff = []
    for i in range(len(closing_prices)):
        diff.append((closing_prices[i]-mean)**2)
    
    return np.sqrt(np.sum(diff)/len(diff))  


## Test 
amazon = stock_df('AMZN','2020-07-25','1d')
plot_prices(amazon, name='Amazon Stocks',interactive = True)
plot_candlestick(amazon,'Amazon')
