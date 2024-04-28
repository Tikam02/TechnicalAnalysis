import streamlit as st
import yfinance as yf
import pandas as pd
import os
import datetime
from Utils.tools import * # Ensure this imports your indicator calculation functions

st.set_page_config(layout="wide")
DATA_DIR = "Data"
PORTFOLIO_FILE = os.path.join(DATA_DIR, "portfolio.csv")

def calculate_returns(stock_name, start_date, end_date, avg_buying_price, quantity):
    try:
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        data = yf.download(stock_name, start=start_date_str, end=end_date_str)
        
        if data.empty:
            st.error(f"No data available for {stock_name} between {start_date_str} and {end_date_str}. Please enter a valid stock symbol and date range.")
            return None, None, None, None, None, None, None, None, None, None, None, None, None
        
        # Calculate indicators
        adr_val = calculate_ADRV(data)
        adr = calculate_ADR(data)
        modified_adr = calculate_modified_ADR(data)
        rsi = calculate_RSI(data)
        sma = calculate_SMA(stock_name, start_date_str, end_date_str)
        two_sma = calculate_200SMA(stock_name, start_date_str, end_date_str)
        ema = calculate_EMA(stock_name, start_date_str, end_date_str)
        
        close_price = data['Close'].values[-1]
        invested_amount = avg_buying_price * quantity
        returns = close_price * quantity
        return_gains = returns - invested_amount
        returns_percentage = ((returns - invested_amount) / invested_amount) * 100

        # Add conditions based on indicators
        buy_sell_adr = 'Buy' if adr.iloc[-1] > 5 else 'Sell'
        buy_sell_rsi = 'Buy' if rsi.iloc[-1] >= 50 else 'Sell'
        bull_bear_sma = 'Bullish' if close_price > sma.iloc[-1] else 'Bearish'
        bull_bear_ema = 'Bullish' if close_price > ema.iloc[-1] else 'Bearish'

        return close_price, invested_amount, returns, returns_percentage, return_gains, adr_val.iloc[-1], adr.iloc[-1], modified_adr.iloc[-1], rsi.iloc[-1], sma.iloc[-1], ema.iloc[-1], buy_sell_adr, buy_sell_rsi, bull_bear_sma, bull_bear_ema
    except Exception as e:
        st.error(f"Error fetching data for {stock_name} between {start_date_str} and {end_date_str}: {str(e)}")
        return None, None, None, None, None, None, None, None, None, None, None, None, None

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
        
        start_date = st.date_input('Enter Start Date:', datetime.date.today() - datetime.timedelta(days=365))
        end_date = datetime.date.today()
        
        if st.button('Add to Portfolio'):
            if stock_name and avg_buying_price and quantity and start_date:
                close_price, invested_amount, returns, returns_percentage, return_gains, adr_val, adr_percentage, modified_adr, rsi, sma, ema, buy_sell_adr, buy_sell_rsi, bull_bear_sma, bull_bear_ema = calculate_returns(stock_name, start_date, end_date, avg_buying_price, quantity)

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
                    'Returns Percentage': f"{returns_percentage:.2f}%",
                    'ADR Value': adr_val,
                    'ADR Percentage': adr_percentage,
                    'Modified ADR': modified_adr,
                    'RSI': rsi,
                    '44 SMA': sma,
                    '25 EMA': ema,
                    'Buy/Sell (ADR)': buy_sell_adr,
                    'Buy/Sell (RSI)': buy_sell_rsi,
                    'Bull/Bear (44 SMA)': bull_bear_sma,
                    'Bull/Bear (25 EMA)': bull_bear_ema
                }
                
                if os.path.exists(PORTFOLIO_FILE):
                    df = pd.read_csv(PORTFOLIO_FILE)
                else:
                    df = pd.DataFrame()

                df = pd.concat([df, pd.DataFrame([portfolio_data])], ignore_index=True)
                df.to_csv(PORTFOLIO_FILE, index=False)
                
                st.success('Added to Portfolio!')
    
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
