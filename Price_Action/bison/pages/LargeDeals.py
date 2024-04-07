import streamlit as st
import pandas as pd
import plotly.express as px
from nsepythonserver import *

# Assuming the nsefetch function is defined in the nsepythonserver module

def nse_largedeals(mode="bulk_deals"):
    payload = nsefetch('https://www.nseindia.com/api/snapshot-capital-market-largedeal')
    if mode == "bulk_deals":
        return pd.DataFrame(payload["BULK_DEALS_DATA"])
    elif mode == "short_deals":
        return pd.DataFrame(payload["SHORT_DEALS_DATA"])
    elif mode == "block_deals":
        return pd.DataFrame(payload["BLOCK_DEALS_DATA"])

def display_dataframe_on_streamlit(df):
    st.dataframe(df)

def plot_buy_sell_vs_qty(df):
    # Get a list of unique symbols
    symbols = df['symbol'].unique()
    
    # Create a dropdown menu for the user to select a symbol
    selected_symbol = st.selectbox("Select a symbol:", symbols)
    
    # Filter the DataFrame for the selected symbol
    symbol_df = df[df['symbol'] == selected_symbol]
    
    # Create a bar chart for the selected symbol
    fig = px.bar(symbol_df, x='buySell', y='qty', title=f'Buy/Sell vs Quantity for {selected_symbol}')
    
    # Show the plot
    st.plotly_chart(fig)

if __name__ == "__main__":
    # Example usage
    st.title("NSE Large Deals Data")
    
    # Select the mode
    mode = st.selectbox("Select the mode:", ["bulk_deals", "short_deals", "block_deals"])
    
    # Fetch and display the data
    df = nse_largedeals(mode)
    display_dataframe_on_streamlit(df)
    
    # Plot Buy/Sell vs Quantity for the selected symbol
    st.header("Buy/Sell vs Quantity")
    plot_buy_sell_vs_qty(df)
