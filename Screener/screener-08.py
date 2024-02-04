import requests
import pandas as pd
import io
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import tkinter as tk
from tkinter import ttk
from tkinter import *

# Function to calculate Exponential Moving Average (EMA)
def calculate_ema(data, column, window):
    return data[column].ewm(span=window, adjust=False, min_periods=window).mean()

# Replace 'path/to/formatted_stock_symbols.txt' with the actual path to your text file
nifty50_file_path = './formatted_stock_symbols.txt'

# Read NIFTY 50 symbols from the text file into a list
with open(nifty50_file_path, 'r') as file:
    nifty50_symbols = [symbol.strip() for symbol in file.readlines()]

# Create the GUI window
root = tk.Tk()
root.title("Stock Analysis")

# Create the Treeview widget
tree = ttk.Treeview(root)
tree["columns"] = ("Price", "25-day MA", "44-day MA", "200-day MA", "25-day EMA", "44-day EMA", "52-wk Low", "52-wk High")

# Define the column headings
tree.heading("#0", text="Symbol")
tree.heading("Price", text="Price")
tree.heading("25-day MA", text="25-day MA")
tree.heading("44-day MA", text="44-day MA")
tree.heading("200-day MA", text="200-day MA")
tree.heading("25-day EMA", text="25-day EMA")
tree.heading("44-day EMA", text="44-day EMA")
tree.heading("52-wk Low", text="52-wk Low")
tree.heading("52-wk High", text="52-wk High")

# Thresholds for filters
moving_avg_threshold = 0.5  # You can adjust this threshold
ema_threshold = 0.5  # You can adjust this threshold

# Iterate over each stock symbol
for ticker_symbol in nifty50_symbols:
    # Your code for each symbol
    try:
        print("Analyzing stock:", ticker_symbol)

        # error handling to remove Jio Financial Services
        if ticker_symbol == 'ITC.NS':
            continue

        # Create a Ticker object
        ticker = yf.Ticker(ticker_symbol)

        # Set the date range for historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        # Get the historical data for the stock within the specified date range
        historical_data = ticker.history(start=start_date, end=end_date)

        # Check if historical data is available for the specified date range
        if historical_data.empty:
            print(f"No historical data available for {ticker_symbol}")
            continue

        # Calculate the moving averages
        historical_data["25MA"] = historical_data["Close"].rolling(window=25).mean()
        historical_data["44MA"] = historical_data["Close"].rolling(window=44).mean()
        historical_data["200MA"] = historical_data["Close"].rolling(window=200).mean()

        # Calculate the Exponential Moving Averages (EMA)
        historical_data["25EMA"] = calculate_ema(historical_data, "Close", 25)
        historical_data["44EMA"] = calculate_ema(historical_data, "Close", 44)

        # Check if 25-day and 44-day EMAs are close
        is_close_emas = (
            abs(historical_data["25EMA"].iloc[-1] - historical_data["44EMA"].iloc[-1]) < ema_threshold
        )

        # Check if 200-day and 44-day SMAs are close
        is_close_smas = (
            abs(historical_data["200MA"].iloc[-1] - historical_data["44MA"].iloc[-1]) < moving_avg_threshold
        )

        # Calculate 52-week low and high based on available data
        low_52_weeks = historical_data["Low"].min()
        high_52_weeks = historical_data["High"].max()

        # Store the results for the current symbol if filters are met
        if is_close_emas and is_close_smas:
            latest_price = historical_data.iloc[-1]["Close"]
            latest_25ma = historical_data.iloc[-1]["25MA"]
            latest_44ma = historical_data.iloc[-1]["44MA"]
            latest_200ma = historical_data.iloc[-1]["200MA"]
            latest_25ema = historical_data.iloc[-1]["25EMA"]
            latest_44ema = historical_data.iloc[-1]["44EMA"]

            # Update the Treeview with the results for the current symbol
            tree.insert("", "end", text=ticker_symbol, values=(
                latest_price, latest_25ma, latest_44ma, latest_200ma, latest_25ema, latest_44ema, low_52_weeks, high_52_weeks))
    except Exception as e:
        print(f"Error analyzing {ticker_symbol}: {e}")

# Pack the Treeview into the GUI
tree.pack(expand=YES, fill=BOTH)

# Start the Tkinter main loop
root.mainloop()
