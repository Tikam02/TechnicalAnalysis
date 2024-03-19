import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate Average Daily Range (ADR)
def calculate_ADR(data):
    data['DailyHigh'] = data['High']
    data['DailyLow'] = data['Low']
    ADR_highlow = (data['DailyHigh'] / data['DailyLow']).rolling(window=14).mean()
    ADR_perc = 100 * (ADR_highlow - 1)
    return ADR_perc

# Function to calculate Modified_ADR as absolute percentage change
def calculate_modified_ADR(data):
    data['dr_pct'] = data.apply(lambda x: 100 * (x["High"] / x["Low"] - 1), axis=1)
    data["mod_adr"] = data['dr_pct'].rolling(window=20).mean()
    return data["mod_adr"]

# Function to apply the scanner conditions
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
def calculate_RSI(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def main():
    st.title('Stock Screener')

    # File selection
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Empty DataFrame to store results
        scanner_results_list = []

        for ticker in df['Symbol']:
            try:
                data = yf.download(ticker, start='2023-01-01', end='2024-03-17')
                data['ADR'] = calculate_ADR(data)
                data['Modified_ADR'] = calculate_modified_ADR(data)
                rsi = calculate_RSI(data)

                results = apply_scanner_conditions(data)
                if results.any():
                    scanner_results_list.append({'Ticker': ticker,
                                                 'Close': round(data['Close'].iloc[-1], 2),
                                                 'ADR': round(data['ADR'].iloc[-1], 2),
                                                 'RSI': round(rsi.iloc[-1], 2),
                                                 'Modified_ADR': round(data['Modified_ADR'].iloc[-1], 2),
                                                 'Volume': round(data['Volume'].iloc[-1], 2)})
            except Exception as e:
                print(f"Error processing {ticker}: {e}")

        # Create DataFrame from results list
        scanner_results = pd.DataFrame(scanner_results_list)

        # Dropdown menu for selecting stocks
        selected_stock = st.selectbox("Select a stock", scanner_results['Ticker'])

        if selected_stock:
            selected_data = yf.download(selected_stock, start='2023-01-01', end='2024-03-17')
            rsi = calculate_RSI(selected_data)
            sma_44 = selected_data['Close'].rolling(window=44).mean()
            ema_25 = selected_data['Close'].ewm(span=25, adjust=False).mean()

            # Plotting the chart
            st.subheader(f"Charts for {selected_stock}")
            fig, ax = plt.subplots()
            ax.plot(selected_data.index, selected_data['Close'], label='Close')
            ax.plot(selected_data.index, sma_44, label='44 SMA')
            ax.plot(selected_data.index, ema_25, label='25 EMA')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax2 = ax.twinx()
            ax2.plot(selected_data.index, rsi, 'r-', label='RSI')
            ax2.set_ylabel('RSI', color='r')
            ax.legend(loc='upper left')
            ax2.legend(loc='upper right')
            st.pyplot(fig)

        # Displaying the results
        st.write(scanner_results)

if __name__ == "__main__":
    main()
