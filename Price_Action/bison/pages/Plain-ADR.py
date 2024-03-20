import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import io

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

# Function to calculate Relative Strength Index (RSI)
def calculate_RSI(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to plot the charts
def plot_charts(data, ticker):
    rsi = calculate_RSI(data)
    sma_44 = data['Close'].rolling(window=44).mean()
    ema_25 = data['Close'].ewm(span=25, adjust=False).mean()

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    ax1.plot(data.index, data['Close'], label='Close')
    ax1.plot(data.index, sma_44, label='44 SMA')
    ax1.set_title(f'{ticker} Price and 44 SMA')
    ax1.legend()

    ax2.plot(data.index, rsi, color='r', label='RSI')
    ax2.axhline(30, linestyle='--', color='r', label='Oversold')
    ax2.axhline(70, linestyle='--', color='r', label='Overbought')
    ax2.set_title('RSI')
    ax2.legend()

    ax3.plot(data.index, data['Close'], label='Close')
    ax3.plot(data.index, ema_25, label='25 EMA')
    ax3.set_title(f'{ticker} Price and 25 EMA')
    ax3.legend()

    plt.tight_layout()
    return fig

def main():
    st.title('Stock Screener')

    # File selection
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Empty DataFrame to store results
        plain_adr_results_list = []

        for ticker in df['Symbol']:
            try:
                data = yf.download(ticker, start='2023-01-01', end='2024-03-17')
                adr = calculate_ADR(data)
                modified_adr = calculate_modified_ADR(data)
                rsi = calculate_RSI(data)

                # Check condition: ADR > 5
                if adr.iloc[-1] > 5:
                    plain_adr_results_list.append({'Stock': ticker,
                                                   'Close': round(data['Close'].iloc[-1], 2),
                                                   'Volume': round(data['Volume'].iloc[-1], 2),
                                                   'ADR': round(adr.iloc[-1], 2),
                                                   'Mod_ADR': round(modified_adr.iloc[-1], 2),
                                                   'RSI': round(rsi.iloc[-1], 2)})
            except Exception as e:
                print(f"Error processing {ticker}: {e}")

        # Create DataFrame from results list
        plain_adr_results_df = pd.DataFrame(plain_adr_results_list)

        # Display the filtered stocks in a table
        st.subheader('Filtered Stocks')
        st.write(plain_adr_results_df)

        # Dropdown menu for selecting stocks
        selected_stock = st.selectbox("Select a stock", plain_adr_results_df['Stock'])

        if selected_stock:
            try:
                selected_data = yf.download(selected_stock, start='2023-01-01', end='2024-03-17')
                fig = plot_charts(selected_data, selected_stock)

                # Display the chart
                st.subheader(f"Charts for {selected_stock}")
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Error processing {selected_stock}: {e}")

if __name__ == "__main__":
    main()