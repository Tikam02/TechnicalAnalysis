import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate Average Daily Range (ADR)
@st.cache_data(ttl=3600)  # Cache the data for 1 hour
def calculate_ADR(data):
    data['DailyHigh'] = data['High']
    data['DailyLow'] = data['Low']
    ADR_highlow = data['DailyHigh'] / data['DailyLow']
    ADR_perc = ADR_highlow.rolling(window=14).apply(lambda x: (x.iloc[-1] / x.iloc[0]) - 1) * 100
    return ADR_perc

# Function to calculate Modified_ADR as absolute percentage change
@st.cache_data(ttl=3600)
def calculate_modified_ADR(data):
    data['dr_pct'] = data['High'].pct_change() * 100
    data['mod_adr'] = data['dr_pct'].rolling(window=20).mean()
    return data['mod_adr']

# Function to apply the scanner conditions
@st.cache_data(ttl=3600)
def apply_scanner_conditions(stock_data):
    adr_above_5 = stock_data['ADR'] > 5
    price_greater_than_1M = stock_data['Close'] > stock_data['Close'].shift(22) * 1.25
    price_greater_than_3M = stock_data['Close'] > stock_data['Close'].shift(67) * 1.5
    price_greater_than_6M = stock_data['Close'] > stock_data['Close'].shift(126) * 2.5
    price_within_15_percent_of_high = stock_data['Close'] >= (stock_data['High'].rolling(window=6).max() * 0.85)
    price_within_15_percent_of_low = stock_data['Close'] <= (stock_data['Low'].rolling(window=6).min() * 1.15)
    stock_data['Dollar_Volume'] = stock_data['Close'] * stock_data['Volume']
    volume_greater_than_3M = stock_data['Dollar_Volume'] > 3000000
    scanner_results = adr_above_5 & price_greater_than_1M & price_greater_than_3M & price_greater_than_6M & \
                      price_within_15_percent_of_high & price_within_15_percent_of_low & volume_greater_than_3M
    return scanner_results

# Function to calculate Relative Strength Index (RSI)
@st.cache_data(ttl=3600)
def calculate_RSI(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).ewm(alpha=1 / window, min_periods=window).mean()
    loss = ((-delta).where(delta < 0, 0)).ewm(alpha=1 / window, min_periods=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to plot the charts
def plot_charts(data, ticker):
    fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    # Price and 44 SMA
    axs[0].plot(data.index, data['Close'], label='Close')
    sma_44 = data['Close'].rolling(window=44).mean()
    axs[0].plot(data.index, sma_44, label='44 SMA')
    axs[0].set_title(f'{ticker} Price and 44 SMA')
    axs[0].legend()

    # RSI
    rsi = calculate_RSI(data)
    axs[1].plot(data.index, rsi, color='r', label='RSI')
    axs[1].axhline(30, linestyle='--', color='r', label='Oversold')
    axs[1].axhline(70, linestyle='--', color='r', label='Overbought')
    axs[1].set_title('RSI')
    axs[1].legend()

    # Price and 25 EMA
    ema_25 = data['Close'].ewm(span=25, adjust=False).mean()
    axs[2].plot(data.index, data['Close'], label='Close')
    axs[2].plot(data.index, ema_25, label='25 EMA')
    axs[2].set_title(f'{ticker} Price and 25 EMA')
    axs[2].legend()

    plt.tight_layout()
    return fig

def main():
    st.title('Qualamaggie ADR Strategy Scanner')

    start_date = st.date_input("Select start date", pd.to_datetime('2023-01-01'))
    end_date = st.date_input("Select end date", pd.to_datetime('2024-03-17'))

    # File selection
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    # Submit button
    if st.button('Submit') and uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Show a spinner while processing the data
        with st.spinner("Processing data..."):
            # Empty DataFrame to store results
            scanner_results_list = []

            for ticker in df['Symbol']:
                try:
                    data = yf.download(ticker, start=start_date, end=end_date)
                    data['ADR'] = calculate_ADR(data)
                    data['Modified_ADR'] = calculate_modified_ADR(data)

                    results = apply_scanner_conditions(data)
                    if results.any():
                        scanner_results_list.append({'Ticker': ticker,
                                                     'Close': round(data['Close'].iloc[-1], 2),
                                                     'ADR': round(data['ADR'].iloc[-1], 2),
                                                     'RSI': round(calculate_RSI(data).iloc[-1], 2),
                                                     'Modified_ADR': round(data['Modified_ADR'].iloc[-1], 2),
                                                     'Volume': round(data['Volume'].iloc[-1], 2)})
                except Exception as e:
                    print(f"Error processing {ticker}: {e}")

        # Create DataFrame from results list
        scanner_results = pd.DataFrame(scanner_results_list)


        # Displaying the results
        st.subheader("Filtered Stocks")
        st.write(scanner_results[['Ticker', 'Close', 'ADR', 'RSI', 'Modified_ADR', 'Volume']])

     
        scanner_results.to_csv("./Data/qm_adr_results.csv", index=False)
        st.success("Results saved to results.csv")
        

if __name__ == "__main__":
    main()