import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Function to get the date of a price
def get_date_of_price(stock_name, target_price, price_range=0.01):
    end_date = datetime.date.today().strftime('%Y-%m-%d')
    data = yf.download(stock_name, start="2000-01-01", end=end_date)
    matching_dates = data[(data['Close'] >= target_price - price_range) & (data['Close'] <= target_price + price_range)].index.tolist()
    if not matching_dates:
        return "No matching date found for the given price."
    return matching_dates[0].strftime('%Y-%m-%d')

# Function to handle the Streamlit app
def main():
    st.title('Stock Price Date Finder')
    
    # Use session state to store the data
    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame()
    
    stock_name = st.text_input('Enter Stock Name:', 'AAPL')
    target_price = st.number_input('Enter Target Price:', 10.00, format="%.2f")
    
    if st.button('Find Date'):
        date = get_date_of_price(stock_name, target_price)
        # Update the session state with the new data
        st.session_state['data'] = pd.DataFrame({
            'Stock Name': [stock_name],
            'Target Price': [target_price],
            'Date': [date]
        })
    
    # Display the data from the session state
    st.write('### Stock Price Dates')
    st.write(st.session_state['data'])

if __name__ == "__main__":
    main()
