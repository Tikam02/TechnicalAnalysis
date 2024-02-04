import requests
import pandas as pd
import io
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import tkinter as tk
from tkinter import ttk
from tkinter import *

# Replace 'path/to/nifty50_symbols.txt' with the actual path to your text file
nifty50_file_path = './nifty50_symbols.txt'

# Read NIFTY 50 symbols from the text file into a list
with open(nifty50_file_path, 'r') as file:
    nifty50_symbols = [symbol.strip() for symbol in file.readlines()]

# Create the GUI window
root = tk.Tk()
root.title("Stock Analysis")

# Create the Treeview widget
tree = ttk.Treeview(root)
tree["columns"] = ("Price", "25-day MA", "44-day MA", "200-day MA", "52-wk Low", "52-wk High")

# Define the column headings
tree.heading("#0", text="Symbol")
tree.heading("Price", text="Price")
tree.heading("25-day MA", text="25-day MA")
tree.heading("44-day MA", text="44-day MA")
tree.heading("200-day MA", text="200-day MA")
tree.heading("52-wk Low", text="52-wk Low")
tree.heading("52-wk High", text="52-wk High")

# Iterate over each stock symbol
for ticker_symbol in nifty50_symbols:
    # Your code for each symbol
    print("Analyzing stock:", ticker_symbol)

    # error handling to remove Jio Financial Services
    if ticker_symbol == 'ITC.NS':
        continue

    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Get the historical data for the stock
    historical_data = ticker.history(period="1y")

    # Get stock information
    stock_info = ticker.info
    mcap = stock_info.get("marketCap")
    sales = stock_info.get("totalRevenue")
    debt_to_equity = stock_info.get("debtToEquity")
    stock_pb = stock_info.get("priceToBook")

    trailing_eps = stock_info.get("trailingEps")

    if trailing_eps is not None and trailing_eps > 0:
        stock_pe = "{:.2f}".format(stock_info.get("currentPrice") / trailing_eps)

    # Calculate the moving averages
    historical_data["25MA"] = historical_data["Close"].rolling(window=25).mean()
    historical_data["44MA"] = historical_data["Close"].rolling(window=44).mean()
    historical_data["200MA"] = historical_data["Close"].rolling(window=200).mean()

    # Get the 52-week high and low
    high_52_weeks = historical_data["Close"].rolling(window=252).max()
    low_52_weeks = historical_data["Close"].rolling(window=252).min()

    # Store the results for the current symbol
    latest_price = historical_data.iloc[-1]["Close"]
    latest_25ma = historical_data.iloc[-1]["25MA"]
    latest_44ma = historical_data.iloc[-1]["44MA"]
    latest_200ma = historical_data.iloc[-1]["200MA"]
    latest_low_52_weeks = low_52_weeks.iloc[-1]
    latest_high_52_weeks = high_52_weeks.iloc[-1]

    # Update the Treeview with the results for the current symbol
    tree.insert("", "end", text=ticker_symbol, values=(
        latest_price, latest_25ma, latest_44ma, latest_200ma, latest_low_52_weeks, latest_high_52_weeks))

# Pack the Treeview into the GUI
tree.pack(expand=YES, fill=BOTH)

# Start the Tkinter main loop
root.mainloop()
