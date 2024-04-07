import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots # Add this line to import make_subplots
from nsepythonserver import *
import logging
from datetime import datetime


current_date = datetime.now().date()

# Assuming the nsefetch function is defined in the nsepythonserver module

def nse_largedeals_historical(from_date, to_date, mode="bulk_deals"):
    if mode == "bulk_deals":
        mode = "bulk-deals"
    elif mode == "short_deals":
        mode = "short-selling"
    elif mode == "block_deals":
        mode = "block-deals"

    url = 'https://www.nseindia.com/api/historical/' + mode + '?from=' + from_date + '&to=' + to_date
    logging.info("Fetching " + str(url))
    payload = nsefetch(url)
    return pd.DataFrame(payload["data"])

def display_dataframe_on_streamlit(df):
    st.dataframe(df)


def plot_buy_sell_vs_qty(df, mode):
    # Create a subplot for each mode
    fig = make_subplots(rows=1, cols=3, subplot_titles=("Block Deals", "Bulk Deals", "Short Deals"))
    fig.update_layout(width=1500, height=700) # Adjust the width and height as needed

    # Plot for Bulk Deals
    if mode == "bulk_deals":
        buy_df = df[df['BD_BUY_SELL'] == 'BUY']
        sell_df = df[df['BD_BUY_SELL'] == 'SELL']
        fig.add_trace(go.Bar(x=buy_df['BD_SYMBOL'], y=buy_df['BD_QTY_TRD'], name='Buy', marker_color='green'), row=1, col=2)
        fig.add_trace(go.Bar(x=sell_df['BD_SYMBOL'], y=sell_df['BD_QTY_TRD'], name='Sell', marker_color='red'), row=1, col=2)
    
    # Plot for Block Deals
    if mode == "block_deals":
        buy_df = df[df['BD_BUY_SELL'] == 'BUY']
        sell_df = df[df['BD_BUY_SELL'] == 'SELL']
        fig.add_trace(go.Bar(x=buy_df['BD_SYMBOL'], y=buy_df['BD_QTY_TRD'], name='Buy', marker_color='green'), row=1, col=1)
        fig.add_trace(go.Bar(x=sell_df['BD_SYMBOL'], y=sell_df['BD_QTY_TRD'], name='Sell', marker_color='red'), row=1, col=1)

    # Plot for Short Deals
    if mode == "short_deals":
        # Assuming 'SS_QTY' is the column that differentiates between buy and sell in short deals
        # Filter the DataFrame to get only sell data
        sell_df = df[df['SS_QTY'] > 0] # Adjust this condition based on how your data differentiates buy and sell
        fig.add_trace(go.Bar(x=sell_df['SS_NAME'], y=sell_df['SS_QTY'], name='Sell', marker_color='red'), row=1, col=3)

    # Update layout
    fig.update_layout(title_text="NSE Large Deals Data", showlegend=True)
    
    # Show the plot
    st.plotly_chart(fig)



if __name__ == "__main__":
    # Example usage
    st.title("NSE Large Deals Data")
    
    # User input for start and end dates
    from_date, to_date = st.date_input("Select a date range", [pd.to_datetime("2024-01-01"), current_date])
    
    # Convert dates to string format expected by the API
    from_date_str = from_date.strftime("%d-%m-%Y")
    to_date_str = to_date.strftime("%d-%m-%Y")

    mode = st.selectbox("Select the mode:", ["bulk_deals", "short_deals", "block_deals"])

    # Fetch and display the data
    df = nse_largedeals_historical(from_date_str, to_date_str, mode)
    display_dataframe_on_streamlit(df)
    
    # Plot Buy/Sell vs Quantity for the selected mode
    st.header("Buy/Sell vs Quantity")
    plot_buy_sell_vs_qty(df, mode)
