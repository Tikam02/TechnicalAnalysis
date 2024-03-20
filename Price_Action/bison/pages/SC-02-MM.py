import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def calculate_RSI(data, window=14):
    delta = data['Adj Close'].diff(1)
    gain = delta.where(delta > 0, 0).ewm(alpha=1 / window, min_periods=window).mean()
    loss = -delta.where(delta < 0, 0).ewm(alpha=1 / window, min_periods=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

@st.cache_data(ttl=3600)  # Cache for 1 hour
def plot_charts(data, ticker):
    fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    # Price and 44 SMA
    axs[0].plot(data.index, data['Adj Close'], label='Close')
    sma_44 = data['Adj Close'].rolling(window=44).mean()
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
    ema_25 = data['Adj Close'].ewm(span=25, adjust=False).mean()
    axs[2].plot(data.index, data['Adj Close'], label='Close')
    axs[2].plot(data.index, ema_25, label='25 EMA')
    axs[2].set_title(f'{ticker} Price and 25 EMA')
    axs[2].legend()

    plt.tight_layout()
    return fig

@st.cache_data(ttl=3600)  # Cache for 1 hour
def check_minervini_conditions(df, rs_df):
    rs_stocks = rs_df['Ticker']
    exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])

    for stock in rs_stocks:
        try:
            sma = [50, 150, 200]
            df[['SMA_50', 'SMA_150', 'SMA_200']] = df['Adj Close'].rolling(window=sma).mean().rename(columns=lambda x: f'SMA_{x}')

            # Storing required values
            currentClose = df["Adj Close"][-1]
            moving_average_50 = df["SMA_50"][-1]
            moving_average_150 = df["SMA_150"][-1]
            moving_average_200 = df["SMA_200"][-1]
            low_of_52week = df["Low"][-260:].min()
            high_of_52week = df["High"][-260:].max()
            RS_Rating = rs_df[rs_df['Ticker'] == stock].RS_Rating.tolist()[0]

            moving_average_200_20 = df["SMA_200"][-20] if len(df) >= 20 else 0

            # Check Minervini conditions
            conditions = [
                currentClose > moving_average_150 > moving_average_200,  # Condition 1
                moving_average_150 > moving_average_200,  # Condition 2
                moving_average_200 > moving_average_200_20,  # Condition 3
                moving_average_50 > moving_average_150 > moving_average_200,  # Condition 4
                currentClose > moving_average_50,  # Condition 5
                currentClose >= (1.3 * low_of_52week),  # Condition 6
                currentClose >= (.75 * high_of_52week)  # Condition 7
            ]

            # If all conditions are true, add stock to exportList
            if all(conditions):
                exportList = exportList.append({'Stock': stock, "RS_Rating": RS_Rating, "50 Day MA": moving_average_50,
                                                "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200,
                                                "52 Week Low": low_of_52week, "52 week High": high_of_52week},
                                               ignore_index=True)
                print(f"{stock} made the Minervini requirements")
        except Exception as e:
            print(e)
            print(f"Could not gather data on {stock}")

    exportList = exportList.sort_values(by='RS_Rating', ascending=False)
    return exportList

def main():
    st.title('Stock Screener')

    # File selection
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        rs_df = pd.read_csv(uploaded_file)  # Assuming the same file contains the RS_Rating column

        # Show a spinner while processing the data
        with st.spinner("Processing data..."):
            exportList = check_minervini_conditions(df, rs_df)

        # Save the output as the input file_name+{MM01}.csv
        file_name = uploaded_file.name.split('.')[0]
        output_file_name = f"{file_name}_MM01.csv"
        exportList.to_csv(output_file_name, index=False)

        # Get the tickers from the "Symbol" column
        tickers = df['Symbol'].tolist()

        # Dropdown menu for selecting stocks
        selected_stock = st.selectbox("Select a stock", tickers)

        if selected_stock:
            stock_data = yf.download(selected_stock, start="2022-01-01", end="2023-04-01")
            fig = plot_charts(stock_data, selected_stock)

            # Display the charts
            st.subheader(f"Charts for {selected_stock}")
            st.pyplot(fig)

        # Displaying the results
        st.subheader("Minervini Stocks")
        st.write(exportList)

if __name__ == "__main__":
    main()