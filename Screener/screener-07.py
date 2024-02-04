import requests
import pandas as pd
import io
import yfinance as yf
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def calculate_emas(prices, short_window, long_window):
    df = pd.DataFrame({'close': prices})
    df['ema_short'] = df['close'].ewm(span=short_window, adjust=False).mean()
    df['ema_long'] = df['close'].ewm(span=long_window, adjust=False).mean()
    return df['ema_short'].iloc[-1], df['ema_long'].iloc[-1]

def analyze_stocks(symbols_file_path, short_window, long_window):
    try:
        # Read symbols from the selected file
        with open(symbols_file_path, 'r') as file:
            symbols = [symbol.strip() for symbol in file.readlines()]

        # Display the symbols in the console
        print("NIFTY Symbols:")
        for symbol in symbols:
            print(symbol)

        # Perform further analysis or display additional information here
        for symbol in symbols:
            # Perform stock analysis here
            # Example: Calculate 25-day and 44-day EMAs for the symbol
            ema_25, ema_44 = calculate_emas(get_stock_prices(symbol), short_window, long_window)
            
            # Example: Display the results in the console
            print(f"\nSymbol: {symbol}")
            print(f"EMA 25: {ema_25}")
            print(f"EMA 44: {ema_44}")

    except Exception as e:
        print(f"Error: {str(e)}")

def get_stock_prices(symbol):
    # Implement fetching historical prices for the given symbol
    # Example: Return a list of closing prices for the last 50 days
    return [100, 105, 110, 115, 120, 125, 130, 135, 140, 145]

# Create the GUI window
root = tk.Tk()
root.title("Stock Analysis")

# Function to get file path and start analysis
def start_analysis():
    symbols_file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt")])

    # Check if a file was selected
    if symbols_file_path:
        short_window = int(entry_short_window.get())
        long_window = int(entry_long_window.get())
        analyze_stocks(symbols_file_path, short_window, long_window)

# Create labels and entry widgets for moving averages
label_short_window = tk.Label(root, text="Enter the short EMA period:")
label_short_window.pack()
entry_short_window = tk.Entry(root)
entry_short_window.pack()

label_long_window = tk.Label(root, text="Enter the long EMA period:")
label_long_window.pack()
entry_long_window = tk.Entry(root)
entry_long_window.pack()

# Create a button to trigger the analysis
analyze_button = ttk.Button(root, text="Analyze Stocks", command=start_analysis)
analyze_button.pack()

# Start the Tkinter main loop
root.mainloop()
