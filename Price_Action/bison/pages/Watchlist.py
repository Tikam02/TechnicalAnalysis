import streamlit as st
from Utils.tools import *
import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
import ta

st.set_page_config(layout="wide")

def color_cells(val):
    """
    Takes a scalar and returns a string with
    the CSS property `'color: red'` for values below 0.5,
    black otherwise.
    """
    color = 'green' if val == 'Buy' or val == 'Bullish' else 'red'
    return 'color: %s' % color

def main():
    st.title('Stock Analysis')

    # Input Form
    st.sidebar.header('Input Form')
    stock_name = st.sidebar.text_input('Stock Name', value='AAPL')
    end_date = st.sidebar.date_input('Date', value=datetime.today())
    start = end_date - timedelta(days=200)

    if st.sidebar.button('Submit'):
        # Download data
        data = yf.download(stock_name, start=start, end=end_date)

        # Check if data is empty
        if not data.empty:
            # Calculate indicators
            adr_val = calculate_ADRV(data)
            adr = calculate_ADR(data)
            modified_adr = calculate_modified_ADR(data)
            rsi = calculate_RSI(data)
            sma = calculate_SMA(stock_name, start, end_date)
            two_sma = calculate_200SMA(stock_name, start, end_date)
            ema = calculate_EMA(stock_name, start, end_date)

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
                '44 SMA': [sma.iloc[-1]],
                '25 EMA': [ema.iloc[-1]]
                # '200 SMA': [two_sma.iloc[-1]]
            })

            # Add columns based on conditions
            latest_data['Buy/Sell (ADR)'] = 'Buy' if latest_data['ADR Percentage'].iloc[0] > 5 else 'Sell'
            latest_data['Buy/Sell (RSI)'] = 'Buy' if latest_data['RSI'].iloc[0] >= 50 else 'Sell'
            latest_data['Bull/Bear (44 SMA)'] = 'Bullish' if latest_data['Close'].iloc[0] > latest_data['44 SMA'].iloc[0] else 'Bearish'
            latest_data['Bull/Bear (25 EMA)'] = 'Bullish' if latest_data['Close'].iloc[0] > latest_data['25 EMA'].iloc[0] else 'Bearish'

            # Save data to watchlist.csv in the "Data" directory
            data_dir = "Data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            watchlist_path = os.path.join(data_dir, 'watchlist.csv')
            if os.path.exists(watchlist_path):
                latest_data.to_csv(watchlist_path, mode='a', header=False, index=False) # Append without header
            else:
                latest_data.to_csv(watchlist_path, index=False) # Write with header
            st.write("Data appended to watchlist.csv")

    # Read data from watchlist.csv if it exists
    watchlist_path = os.path.join("Data", "watchlist.csv")
    if os.path.exists(watchlist_path):
        st.subheader('Data from watchlist')
        watchlist_data = pd.read_csv(watchlist_path)
        
        # Apply styling to the DataFrame
        #styled_data = watchlist_data.style.applymap(color_cells)
        styled_data = watchlist_data.style.applymap(color_cells, subset=['Buy/Sell (ADR)', 'Buy/Sell (RSI)','Bull/Bear (44 SMA)','Bull/Bear (25 EMA)'])

        
        
        # Display the styled DataFrame
        st.table(styled_data)

if __name__ == '__main__':
    main()
