import streamlit as st
import yfinance as yf
import pandas as pd
import os
import datetime
from Utils.tools import *

st.set_page_config(layout="wide")
DATA_DIR = "Data"
PORTFOLIO_FILE = os.path.join(DATA_DIR, "portfolio.csv")

def calculate_returns(stock_name, start_date, end_date, avg_buying_price, quantity):
    try:
        # Convert datetime.date objects to strings in the format expected by yf.download
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # Use yf.download to fetch stock data
        data = yf.download(stock_name, start=start_date_str, end=end_date_str)
        
        # Check if data is empty
        if data.empty:
            st.error(f"No data available for {stock_name} between {start_date_str} and {end_date_str}. Please enter a valid stock symbol and date range.")
            return None, None, None, None
        
        close_price = data['Close'].values[-1] # Use the last close price
        invested_amount = avg_buying_price * quantity
        returns = close_price * quantity
        return_gains = returns - invested_amount
        returns_percentage = ((returns - invested_amount) / invested_amount) * 100

        return close_price, invested_amount, returns, returns_percentage,return_gains
    except Exception as e:
        st.error(f"Error fetching data for {stock_name} between {start_date_str} and {end_date_str}: {str(e)}")
        return None, None, None, None

def main():
    st.title('Stock Portfolio Tracker')
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    total_invested_amount = 0
    total_gains = 0
    
    
    with st.sidebar:
        st.header('Add Stock')
        stock_name = st.text_input('Enter Stock Name:')
        avg_buying_price = st.number_input('Enter Average Buying Price:')
        quantity = st.number_input('Enter Quantity:', min_value=1)
        
        
        # User input for start date
        start_date = st.date_input('Enter Start Date:', datetime.date.today() - datetime.timedelta(days=365))
        
        # End date is always the current date
        end_date = datetime.date.today()
        
        
        if st.button('Add to Portfolio'):
            if stock_name and avg_buying_price and quantity and start_date:
                close_price, invested_amount, returns, returns_percentage,return_gains = calculate_returns(stock_name, start_date, end_date, avg_buying_price, quantity)

                portfolio_data = {
                    'Stock Name': stock_name,
                    'Start Date': start_date,
                    'End Date': end_date,
                    'Average Buying Price': avg_buying_price,
                    'Quantity': quantity,
                    'Current Price': close_price,
                    'Invested Amount': f"{invested_amount:.2f}",
                    'Total Loss/Gain': f"{returns:.2f}",
                    'Returns Loss/Gains': f"{return_gains:.2f}",
                    'Returns Percentage': f"{returns_percentage:.2f}%"
                }
                
                if os.path.exists(PORTFOLIO_FILE):
                    df = pd.read_csv(PORTFOLIO_FILE)
                else:
                    df = pd.DataFrame()

                df = pd.concat([df, pd.DataFrame([portfolio_data])], ignore_index=True)
                df.to_csv(PORTFOLIO_FILE, index=False)
                
                st.success('Added to Portfolio!')
    
    # Display portfolio table
    if os.path.exists(PORTFOLIO_FILE):
        df = pd.read_csv(PORTFOLIO_FILE)
        st.write('## Portfolio Summary')
        st.write('### Portfolio')
        st.write(df)
        
        total_invested_amount = df['Invested Amount'].sum()
        total_gains = df['Total Loss/Gain'].sum()
        
        st.write('### Total Invested Amount:', total_invested_amount)
        st.write('### Total Gains:', total_gains)
        st.write('### Total Gain Percentage:', ((total_gains - total_invested_amount) / total_invested_amount) * 100)
        
        


if __name__ == '__main__':
    main()
