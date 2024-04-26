import streamlit as st
from Utils.tools import *
import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
import ta

def main():
    st.title('Stock Analysis')

    # Input Form
    st.sidebar.header('Input Form')
    stock_name = st.sidebar.text_input('Stock Name', value='AAPL')
    end_date = st.sidebar.date_input('Date', value=datetime.today())
    start=end_date - timedelta(days=200)

    if st.sidebar.button('Submit'):
        # Download data
        data = yf.download(stock_name, start=end_date - timedelta(days=90), end=end_date)
        # print("Data",data)
    
        # Check if data is empty
        if not data.empty:
            # Calculate indicators
            adr_val = calculate_ADRV(data)
            adr = calculate_ADR(data)
            modified_adr = calculate_modified_ADR(data)
            rsi = calculate_RSI(data)
            sma = calculate_SMA(stock_name,start,end_date)
            two_sma = calculate_200SMA(stock_name,start,end_date)
            ema = calculate_EMA(stock_name,start,end_date)

    
            # Get the latest data (last row)
            latest_data = pd.DataFrame({
                'Date': [data.index[-1]],
                'Symbol': [stock_name],
                'Close': [data.Close.iloc[-1]],
                'Volume': [data.Volume.iloc[-1]],
                'ADR Value': [adr_val.iloc[-1]],
                'ADR Percentage': [adr.iloc[-1]],
                'Modified ADR': [modified_adr.iloc[-1]],
                'RSI': [rsi.iloc[-1]],
                '44 SMA':[sma.iloc[-1]],
                '25 EMA':[ema.iloc[-1]],
                '200 SMA': [two_sma.iloc[-1]]
            })

            # Display the latest data in a table
            st.subheader('Latest Data')
            st.write(latest_data)

            # Save data to watchlist.csv in the "Data" directory
            data_dir = "Data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            watchlist_path = os.path.join(data_dir, 'watchlist.csv')
            if os.path.exists(watchlist_path):
                latest_data.to_csv(watchlist_path, mode='a', header=False, index=False)  # Append without header
            else:
                latest_data.to_csv(watchlist_path, index=False)  # Write with header
            st.write("Data appended to watchlist.csv")

    # Read data from watchlist.csv if it exists
    watchlist_path = os.path.join("Data", "watchlist.csv")
    if os.path.exists(watchlist_path):
        st.subheader('Data from watchlist.csv')
        watchlist_data = pd.read_csv(watchlist_path)
        st.write(watchlist_data)

if __name__ == '__main__':
    main()
