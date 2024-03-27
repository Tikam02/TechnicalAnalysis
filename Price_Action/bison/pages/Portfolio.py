import streamlit as st
import pandas as pd
import yfinance as yf
import os

# Function to fetch stock data
def get_stock_data(stock_name):
    stock = yf.Ticker(stock_name)
    return stock.history(period="1d")

# Function to calculate Average Price, Investment Amount, Return Since Bought, and Profit/Loss
def calculate_metrics(buy_price, buy_quantity, current_price):
    average_price = buy_price / buy_quantity
    investment_amount = buy_price * buy_quantity
    amount_gained = (current_price - average_price) * buy_quantity
    percentage_gain = (amount_gained / investment_amount) * 100
    profit_loss = current_price * buy_quantity - investment_amount
    return average_price, investment_amount, percentage_gain, amount_gained, profit_loss

# Function to calculate ADR
def calculate_ADR(data):
    data['DailyHigh'] = data['High']
    data['DailyLow'] = data['Low']
    ADR_highlow = data['DailyHigh'] / data['DailyLow']
    ADR_perc = ADR_highlow.rolling(window=14).apply(lambda x: (x.iloc[-1] / x.iloc[0]) - 1) * 100
    return ADR_perc

# Function to save portfolio data to CSV
def save_to_csv(portfolio_data):
    portfolio_df = pd.DataFrame(portfolio_data)
    portfolio_df.to_csv('portfolio.csv', index=False)

# Function to read portfolio data from CSV
def read_from_csv():
    if 'portfolio.csv' in os.listdir():
        return pd.read_csv('portfolio.csv')
    else:
        return pd.DataFrame(columns=['Stock Name', 'Buy Price', 'Buy Quantity'])

# Main function
def main():
    st.title('Stock Portfolio Management')

    # Input section
    st.subheader('Add Stock Details')
    stock_name = st.text_input('Enter Stock Name:')
    buy_price = st.number_input('Enter Buy Price:', min_value=0.01)
    buy_quantity = st.number_input('Enter Buy Quantity:', min_value=1)

    # Read portfolio data
    portfolio_data = read_from_csv()

    # Display stock metrics
    if stock_name:
        stock_data = get_stock_data(stock_name)
        if not stock_data.empty:
            current_price = stock_data['Close'].iloc[-1]
            average_price, investment_amount, percentage_gain, amount_gained, profit_loss = calculate_metrics(buy_price, buy_quantity, current_price)
            adr = calculate_ADR(stock_data)

            # Update portfolio data
            portfolio_data = portfolio_data.append({'Stock Name': stock_name, 'Buy Price': buy_price, 'Buy Quantity': buy_quantity}, ignore_index=True)
            save_to_csv(portfolio_data)

            # Display metrics in a table
            st.subheader('Stock Metrics')
            metrics_data = {
                'Metric': ['Average Price', 'Investment Amount', 'Return Since Bought (%)', 'Amount Gained', 'Profit/Loss'],
                'Value': [average_price, investment_amount, percentage_gain, amount_gained, profit_loss]
            }
            metrics_df = pd.DataFrame(metrics_data)
            st.write(metrics_df)

            # Display ADR and other metrics
            st.subheader('Other Metrics')
            st.write(f"Current Market Price: {current_price}")
            st.write(f"ADR (Average Daily Range): {adr.iloc[-1]}")
            # Add more metrics as needed

    # Display portfolio data
    st.subheader('Portfolio')
    st.write(portfolio_data)

if __name__ == "__main__":
    main()
