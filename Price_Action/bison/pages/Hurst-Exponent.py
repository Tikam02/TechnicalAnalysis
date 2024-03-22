import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf

def hurst_fd(price_series, min_window=10, max_window=100, num_windows=20, num_samples=100):
    """
    Calculates the Hurst Exponent and Fractal Dimension of a time series.
    """
    try:
        log_returns = np.diff(np.log(price_series))

        window_sizes = np.linspace(min_window, max_window, num_windows, dtype=int)
        R_S = []

        for w in window_sizes:
            R, S = [], []
            for _ in range(num_samples):
                start = np.random.randint(0, len(log_returns) - w)
                seq = log_returns[start:start + w]
                R.append(np.max(seq) - np.min(seq))
                S.append(np.std(seq))
            R_S.append(np.mean(R) / np.mean(S))

        log_window_sizes = np.log(window_sizes)
        log_R_S = np.log(R_S)
        coeffs = np.polyfit(log_window_sizes, log_R_S, 1)

        hurst_exponent = coeffs[0]
        fractal_dimension = 2 - hurst_exponent

        return hurst_exponent, fractal_dimension
    except (ValueError, RuntimeWarning):
        return np.nan, np.nan

def calculate_hurst_exponent(log_returns):
    """
    Calculates the Hurst exponent for a given series of log returns.
    """
    # Initialize the range of scales to consider
    scales = range(10, len(log_returns) + 1, 10)

    # Initialize an empty list to store the Hurst exponents
    hurst_exponents = []

    # Calculate the Hurst exponent for each scale
    for scale in scales:
        # Calculate the cumulative sum of the log returns
        cumulative_sum = np.cumsum(log_returns[:scale])

        # Calculate the range of the cumulative sum
        R = np.max(cumulative_sum) - np.min(cumulative_sum)

        # Calculate the standard deviation of the log returns
        std = np.std(log_returns[:scale])

        # Calculate the Hurst exponent for this scale
        H = np.log(R) / np.log(std * np.sqrt(scale))

        # Add the Hurst exponent to the list
        hurst_exponents.append(H)

    # Calculate the mean Hurst exponent over all scales
    hurst_exponent = np.mean(hurst_exponents)

    return hurst_exponent

def rolling_hurst(price_series, window, min_window=10, max_window=100, num_windows=20, num_samples=100):
    """
    Calculates the rolling Hurst Exponent of a time series.
    """
    return price_series.rolling(window=window).apply(lambda x: calculate_hurst_exponent(x), raw=True)

def rolling_fractal_dimension(price_series, window, min_window=10, max_window=100, num_windows=20, num_samples=100):
    """
    Calculates the rolling Fractal Dimension of a time series.
    """
    return price_series.rolling(window=window).apply(lambda x: hurst_fd(x, min_window, max_window, num_windows, num_samples)[1], raw=True)

# Streamlit app
st.title("Stock Hurst Exponent and Trend Analysis")

# User input for stock tickers
num_stocks = st.number_input("Enter the number of stocks", min_value=1, step=1, value=1)
stock_tickers = [st.text_input(f"Enter Stock Ticker {i}", key=f"ticker_{i}", value=f"Stock {i}") for i in range(1, num_stocks + 1)]

# Calculate Hurst exponent and plot trends for each stock
for stock_ticker in stock_tickers:
    try:
        stock_data = yf.Ticker(stock_ticker.upper()).history(period="max")
        close_prices = stock_data["Close"].values
        log_returns = np.log(close_prices[1:] / close_prices[:-1])
        hurst_exponent, fractal_dimension = hurst_fd(log_returns)

        st.write(f"Hurst Exponent for {stock_ticker}: {hurst_exponent:.2f}")

        # Plot stock trend
        st.subheader(f"Trend in {stock_ticker}")
        st.line_chart(stock_data["Close"])

        # Plot rolling Hurst Exponent
        st.subheader("Rolling Hurst Exponent")
        rolling_window = st.slider("Select Rolling Window Size", min_value=10, max_value=100, step=10, value=50)
        hurst_values = rolling_hurst(pd.Series(close_prices), rolling_window)
        st.line_chart(hurst_values)

        # Plot rolling Fractal Dimension
        st.subheader("Rolling Fractal Dimension")
        fractal_values = rolling_fractal_dimension(pd.Series(close_prices), rolling_window)
        st.line_chart(fractal_values)

    except Exception as e:
        st.write(f"Error for {stock_ticker}: {e}")
