import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Constants
PERIODS = [30, 60, 90]

def fetch_data(ticker_symbol, start_date, end_date):
    """Fetches historical data for a given ticker symbol."""
    ticker_data = yf.Ticker(ticker_symbol)
    return ticker_data.history(period='1d', start=start_date, end=end_date)

def calculate_z_scores(close_prices, periods):
    """Calculates Z-scores for given periods."""
    z_scores_dict = {}
    for period in periods:
        # Calculate the rolling mean for the given period
        rolling_mean = close_prices.rolling(window=period).mean()      
        # Calculate the rolling standard deviation for the given period
        rolling_std = close_prices.rolling(window=period).std()       
        # Compute the Z-scores for the close prices
        z_scores = (close_prices - rolling_mean) / rolling_std      
        # Store the Z-scores in the dictionary with the period as the key
        z_scores_dict[period] = z_scores
    return z_scores_dict

def plot_data(close_prices, z_scores_data, ticker_symbol, z_thresh):
    """Plots close prices and z-scores."""   
    
    # Create subplots for close prices and Z-scores
    fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(20, 8))   
    
    # Plot the close prices on the first subplot
    ax1.plot(close_prices.index, close_prices, label='Close Prices')
    for period, z_scores in z_scores_data.items():
        # Plot the Z-scores on the second subplot for each period
        ax2.plot(z_scores.index, z_scores, label=f'Z-Scores {period} days', alpha=0.7)       
        # If the period is the first in the list, plot buy/sell signals on the first subplot
        if period == PERIODS[0]:
            buy_signals = (z_scores < -z_thresh)
            sell_signals = (z_scores > z_thresh)
            ax1.plot(close_prices[buy_signals].index, close_prices[buy_signals], 'o', color='g', label='Buy Signal')
            ax1.plot(close_prices[sell_signals].index, close_prices[sell_signals], 'o', color='r', label='Sell Signal')
    # Set the y-label and legend for the close prices subplot
    ax1.set_ylabel('Close Prices')
    ax1.legend(loc="upper left")
    ax1.grid(True)
    
    # Draw horizontal lines indicating the Z-score thresholds on the Z-scores subplot
    ax2.axhline(-z_thresh, color='red', linestyle='--')
    ax2.axhline(z_thresh, color='red', linestyle='--')   
    # Set the y-label and legend for the Z-scores subplot
    ax2.set_ylabel('Z-Scores')
    ax2.legend(loc="upper left")
    ax2.grid(True)

    # Set the main title for the entire plot
    plt.suptitle(f'{ticker_symbol} Close Prices and Z-Scores (Z threshold = {z_thresh})')

    # Display the plots using Streamlit
    st.pyplot(fig)

def main():
    st.title("Stock Analysis")

    # User inputs
    ticker_symbol = st.text_input("Enter Ticker Symbol", "BCLIND.NS")
    start_date = st.date_input("Start Date", value=pd.to_datetime('2022-01-01'))
    end_date = st.date_input("End Date", value=pd.to_datetime('2024-03-11'))
    z_thresh = st.slider("Z Threshold", min_value=0, max_value=10, value=2)

    # Fetch the historical data for the ticker symbol
    ticker_data = fetch_data(ticker_symbol, start_date, end_date)

    # Calculate Z-scores for the specified periods
    z_scores_data = calculate_z_scores(ticker_data['Close'], PERIODS)

    # Plot the close prices and Z-scores
    plot_data(ticker_data['Close'], z_scores_data, ticker_symbol, z_thresh)

if __name__ == "__main__":
    main()

