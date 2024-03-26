import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from talib.abstract import *
from datetime import date
import mplfinance as mpf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import io
import talib as ta


# Function to calculate Squeeze Momentum Indicator and plot the chart
def calculate_and_plot_squeeze_momentum(symbol, start_date, end_date):
    # Fetch data from Yahoo Finance
    df = yf.download(symbol, start=start_date, end=end_date)

    # Parameter setup
    length = 20
    mult = 2
    length_KC = 20
    mult_KC = 1.5

    # Calculate BB
    m_avg = df['Close'].rolling(window=length).mean()
    m_std = df['Close'].rolling(window=length).std(ddof=0)
    df['upper_BB'] = m_avg + mult * m_std
    df['lower_BB'] = m_avg - mult * m_std

    # Calculate true range
    df['tr0'] = abs(df["High"] - df["Low"])
    df['tr1'] = abs(df["High"] - df["Close"].shift())
    df['tr2'] = abs(df["Low"] - df["Close"].shift())
    df['tr'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)

    # Calculate KC
    range_ma = df['tr'].rolling(window=length_KC).mean()
    df['upper_KC'] = m_avg + range_ma * mult_KC
    df['lower_KC'] = m_avg - range_ma * mult_KC

    # Calculate bar value
    highest = df['High'].rolling(window=length_KC).max()
    lowest = df['Low'].rolling(window=length_KC).min()
    m1 = (highest + lowest) / 2
    df['value'] = (df['Close'] - (m1 + m_avg) / 2)
    fit_y = np.array(range(0, length_KC))
    df['value'] = df['value'].rolling(window=length_KC).apply(lambda x: 
        np.polyfit(fit_y, x, 1)[0] * (length_KC-1) + np.polyfit(fit_y, x, 1)[1], raw=True)

    # Check for 'squeeze'
    df['squeeze_on'] = (df['lower_BB'] > df['lower_KC']) & (df['upper_BB'] < df['upper_KC'])
    df['squeeze_off'] = (df['lower_BB'] < df['lower_KC']) & (df['upper_BB'] > df['upper_KC'])

    # Take only the last 100 rows of data
    df = df[-100:]

    # Extract only ['Open', 'High', 'Close', 'Low'] from df
    ohcl = df[['Open', 'High', 'Close', 'Low']]

    # Add colors for the 'value bar'
    colors = []
    for ind, val in enumerate(df['value']):
        if val >= 0:
            color = 'green'
            if val > df['value'][ind - 1]:
                color = 'lime'
        else:
            color = 'maroon'
            if val < df['value'][ind - 1]:
                color = 'red'
        colors.append(color)

    # Add subplots: 1. bars, 2. crosses
    apds = [mpf.make_addplot(df['value'], panel=1, type='bar', color=colors, alpha=0.8, secondary_y=False),
            mpf.make_addplot([0] * len(df), panel=1, type='scatter', marker='x', markersize=50,
                             color=['gray' if s else 'black' for s in df['squeeze_off']], secondary_y=False)]

    # Plot OHLC with subplots
    fig, axes = mpf.plot(ohcl, volume_panel=2, figratio=(2, 1), figscale=1, type='candle', addplot=apds,
                         returnfig=True)

    # Display the figure
    st.pyplot(fig)


# Function to get technical indicators
def get_technical_indicators(data):
    # Bollinger Bands
    data['upper_band'], data['middle_band'], data['lower_band'] = BBANDS(data['Close'], timeperiod=20)

    # MACD
    data['macd'], data['macd_signal'], _ = MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    # RSI
    data['rsi'] = RSI(data['Close'], timeperiod=14)

    # Simple Moving Averages
    data['sma_44'] = SMA(data['Close'], timeperiod=44)
    data['sma_25'] = SMA(data['Close'], timeperiod=25)

    return data

# Function to fetch data from Yahoo Finance and plot candlestick chart with MAV
def plot_candlestick_with_mav(symbol, start_date, end_date, mav=None, volume=False):
    # Fetch data from Yahoo Finance
    df = yf.download(symbol, start=start_date, end=end_date)

        # Plot candlestick chart with MAV
    if volume:
        addplot = mpf.make_addplot(df['Volume'], panel=1, ylabel='Volume', color='b')
    else:
        addplot = []

    # Plot candlestick chart with Moving Averages
    mpf.plot(df, type='candle', mav=mav,style='starsandstripes', volume=volume, addplot=addplot,figratio=(25,20),figscale=4,ylabel='OHLC Candles',ylabel_lower='Shares\nTraded',xlabel='DATE', returnfig=True,)
    plt.title('Candlestick Chart with Moving Averages')
    # Save the plot as an image
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()

    # Display the saved image using Streamlit
    st.image(img_bytes.getvalue())



# Streamlit app
st.title("Stock Technical Analysis")

# User input for stock symbol, start date, and end date
symbol = st.text_input("Enter Stock Symbol", value="AAPL")
start_date = st.date_input("Enter Start Date", value=date.today().replace(year=date.today().year - 1))
end_date = st.date_input("Enter End Date", value=date.today())

if st.button("Submit"):
    # Fetch historical data
    data = yf.download(symbol, start=start_date, end=end_date)
    calculate_and_plot_squeeze_momentum(symbol, start_date, end_date)

    # Fetch data from Yahoo Finance
    df = yf.download(symbol, start=start_date, end=end_date)
    
    # Calculate SMA-50 and SMA-200
    df['SMA-50'] = ta.SMA(df['Close'], timeperiod=50)
    df['SMA-200'] = ta.EMA(df['Close'], timeperiod=200)
    
    # Construct a 2 x 1 Plotly figure
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.01, shared_xaxes=True)
    
    # Plot the Price, SMA-50, and SMA-200 chart
    for col in ['Close', 'SMA-50', 'SMA-200']:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col), row=1, col=1)
    
    # Change the Close to Price for the legend label
    fig.data[0].name = 'Price'

    # Button to plot candlestick chart with MAV (25)
    plot_candlestick_with_mav(symbol, start_date, end_date, mav=25)


    # Button to plot candlestick chart with MAV (8, 20, 50) and volume
    plot_candlestick_with_mav(symbol, start_date, end_date, mav=(25, 44, 200), volume=True)

    # Calculate technical indicators
    data = get_technical_indicators(data)

    # Plotting
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(14, 10), sharex=True)

    # Plot Bollinger Bands
    axes[0].plot(data['Close'], label='Close Price', color='blue')
    axes[0].plot(data['upper_band'], label='Upper Bollinger Band', color='orange')
    axes[0].plot(data['middle_band'], label='Middle Bollinger Band', color='black')
    axes[0].plot(data['lower_band'], label='Lower Bollinger Band', color='orange')
    axes[0].set_title('Bollinger Bands')
    axes[0].legend()

    # Plot MACD
    axes[1].plot(data['macd'], label='MACD', color='blue')
    axes[1].plot(data['macd_signal'], label='MACD Signal', color='red')
    axes[1].set_title('MACD')
    axes[1].legend()

    # Plot RSI
    axes[2].plot(data['rsi'], label='RSI', color='blue')
    axes[2].axhline(70, linestyle='--', color='red')
    axes[2].axhline(30, linestyle='--', color='red')
    axes[2].set_title('RSI')
    axes[2].legend()

  

    # Show plots
    st.pyplot(fig)




