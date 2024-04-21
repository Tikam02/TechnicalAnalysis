import streamlit as st
import pandas as pd
import yfinance as yf
import talib

# Function to get stock data
def get_stock_data(stock_name):
    try:
        stock = yf.Ticker(stock_name)
        data = stock.history(period="1mo")
        data['RSI'] = talib.RSI(data['Close'])
        data['ADR'] = (data['High'] - data['Low']) / data['Close'] * 100
        return data
    except:
        return None

# Streamlit app
def main():
    st.title('Stock Analysis App')
    
    # Input form
    stock_name = st.text_input('Enter Stock Name:')
    if st.button('Submit'):
        if stock_name:
            stock_data = get_stock_data(stock_name)
            if stock_data is not None:
                # Display table
                st.write(stock_data[['RSI', 'ADR', 'Close', 'Volume']])
            else:
                st.error('Error: Unable to retrieve data. Please enter a valid stock name.')

if __name__ == "__main__":
    main()
