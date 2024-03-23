import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from talib.abstract import *
from datetime import date

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

# Streamlit app
st.title("Stock Technical Analysis")

# User input for stock symbol, start date, and end date
symbol = st.text_input("Enter Stock Symbol", value="AAPL")
start_date = st.date_input("Enter Start Date", value=date.today().replace(year=date.today().year - 1))
end_date = st.date_input("Enter End Date", value=date.today())

if st.button("Submit"):
    # Fetch historical data
    data = yf.download(symbol, start=start_date, end=end_date)

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
