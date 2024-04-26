import streamlit as st
import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
import ta
import warnings
from nsepython import *


## data = yf.download(ticker, start=start_date, end=end_date)

# Function to calculate ADR Values
def calculate_ADRV(data):
    # Calculate the daily range (High - Low) using a lambda function
    data['dr'] = data.apply(lambda x: x["High"] - x["Low"], axis=1)
    
    # Calculate the average daily range (ADR) over a 20-period interval
    data["adr"] = data['dr'].rolling(window=14).mean()
    
    return data["adr"]

# Function to calculate Average Daily Range (ADR) Percentage
def calculate_ADR(data):
    data['DailyHigh'] = data['High']
    data['DailyLow'] = data['Low']
    ADR_highlow = (data['DailyHigh'] / data['DailyLow']).rolling(window=14).mean()
    ADR_perc = 100 * (ADR_highlow - 1)
    return ADR_perc

# Function to calculate Modified_ADR as absolute percentage change
def calculate_modified_ADR(data):
    data['dr_pct'] = data.apply(lambda x: 100 * (x["High"] / x["Low"] - 1), axis=1)
    data["mod_adr"] = data['dr_pct'].rolling(window=20).mean()
    return data["mod_adr"]

# Function to calculate Relative Strength Index (RSI)
def calculate_RSI(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate beta 
# Beta = Covariance/Variance
# Covariance is the measure of a stock/index’s return relative to the market.
# Variance is the measure of how the market moves relative to its mean.



def calculate_EMA(symbol, start_date, end_date, window=25):
    # Download historical data
    data = yf.download(symbol, start=start_date, end=end_date)
    if data.empty:
        return None  # Return None if no data is available

    # Calculate EMA
    ema = ta.trend.ema_indicator(data['Close'], window=window)
    return ema

def calculate_SMA(symbol, start_date, end_date, window=44):
    # Download historical data
    data = yf.download(symbol, start=start_date, end=end_date)
    if data.empty:
        return None  # Return None if no data is available

    # Calculate SMA
    sma = ta.trend.sma_indicator(data['Close'], window=window)
    return sma


def calculate_200SMA(symbol, start_date, end_date, window=200):
    # Download historical data
    data = yf.download(symbol, start=start_date, end=end_date)
    if data.empty:
        return None  # Return None if no data is available

    # Calculate SMA
    sma = ta.trend.sma_indicator(data['Close'], window=window)
    return sma


