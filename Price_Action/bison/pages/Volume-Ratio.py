import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def main():
    st.title("Stock Analysis")

    # Input field for ticker symbol
    ticker = st.text_input("Enter Ticker Symbol", value='BCLIND.NS')

    # Check if the user has entered a ticker symbol
    if ticker:
        # Define the percentile threshold
        percentile_threshold = 0.97

        # Fetch the data
        data = yf.download(ticker, start='2023-01-01', end='2024-03-11')

        # Compute moving averages
        data['50_day_MA'] = data['Close'].rolling(window=50).mean()
        data['200_day_MA'] = data['Close'].rolling(window=200).mean()

        # Compute volume ratio and moving average
        data['Volume_MA20'] = data['Volume'].rolling(window=20).mean()
        data['Volume_Ratio'] = data['Volume'] / data['Volume_MA20']

        # Calculate the dynamic percentile threshold
        dynamic_percentile = data['Volume_Ratio'].quantile(percentile_threshold)
        mask = data['Volume_Ratio'] > dynamic_percentile

        # Create subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(30, 14))

        # Plot Close Price on ax1
        ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
        ax1.scatter(data.index[mask], data['Close'][mask], color='red', s=100, label='High Volume Ratio')
        ax1.set_title(f'{ticker} Stock Price (2020-2023)')
        ax1.set_ylabel('Price')
        ax1.legend(loc='upper left')

        # Create a secondary y-axis for volume
        ax1b = ax1.twinx()
        ax1b.bar(data.index, data['Volume'], color='gray', alpha=0.3, label='Volume')
        ax1b.plot(data.index, data['Volume_MA20'], color='purple', label='20-day Volume MA', alpha=0.3)  
        ax1b.set_ylabel('Volume')
        ax1b.legend(loc='lower left')

        # Plot Volume Ratio on ax2
        ax2.plot(data.index, data['Volume_Ratio'], label='Volume Ratio', color='green')
        ax2.axhline(y=dynamic_percentile, color='red', linestyle='--', label=f'{percentile_threshold*100:.0f}% percentile')
        ax2.set_title(f'Volume Ratio Over Time for {ticker}')
        ax2.set_ylabel('Volume Ratio')
        ax2.legend(loc='upper left')

        # Plot histogram of Volume Ratio values on ax3
        ax3.hist(data['Volume_Ratio'], bins=50, color='green', alpha=0.7, label='Volume Ratio Distribution')
        ax3.axvline(x=dynamic_percentile, color='red', linestyle='--', label=f'{percentile_threshold*100:.0f}% percentile')
        ax3.set_title(f'Histogram of Volume Ratio for {ticker}')
        ax3.set_xlabel('Volume Ratio')
        ax3.set_ylabel('Frequency')
        ax3.legend(loc='upper left')

        # Display plots
        st.pyplot(fig)

if __name__ == "__main__":
    main()
