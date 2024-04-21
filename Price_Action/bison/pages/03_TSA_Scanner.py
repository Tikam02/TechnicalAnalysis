import streamlit as st
import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta
import ta
import warnings

# Ignore FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Define the path to the data folder
DATA_FOLDER = "./Data"
six_months_ago = datetime.now() - timedelta(days=30*6)
one_year_ago = datetime.now() - timedelta(days=365)


# Combined function to apply scanner conditions
def apply_scanner_conditions(stock_data):
    # Calculate 52-week high and low
    lo = stock_data['Low'].min()
    hi = stock_data['High'].max()

    # Calculate thresholds for conditions 6 and 7
    x = 1.3 * lo # 30% above its 52-week low
    y = 0.75 * hi # 25% of its 52-week high


    # Calculate RSI
    stock_data['RSI'] = ta.momentum.rsi(stock_data['Close'])

    # Precompute rolling means for different window sizes
    rolling_means = {
        '200': stock_data['Close'].rolling(window=200).mean(),
        '150': stock_data['Close'].rolling(window=150).mean(),
        '50': stock_data['Close'].rolling(window=50).mean(),
    }
    
    conditions = (
    (stock_data['Close'].iloc[-1] > rolling_means['200'].iloc[-1]) &  ## close > 200 SMA
    (rolling_means['150'].iloc[-1] > rolling_means['200'].iloc[-1]) & ## 150 SMA > 200
    (rolling_means['50'].iloc[-1] > rolling_means['150'].iloc[-1]) &  ## 50 SMA > 150
    (stock_data['Close'].iloc[-1] > x) & ## close > 30% above 52 Week low
    (stock_data['Close'].iloc[-1] > y) & ## close > 25% above 52 week high
    (stock_data['Close'].iloc[-1] > 1.25 * stock_data['Close'].shift(22).iloc[-1]) & ## close > 25% Greater than 22 Days ago
    (stock_data['Close'].iloc[-1] > 1.5 * stock_data['Close'].shift(67).iloc[-1]) &  ## close >  50% Greater than 67 Days ago
    (stock_data['Close'].iloc[-1] > 2.5 * stock_data['Close'].shift(126).iloc[-1]) ## close > 150% Greater than 126 Days ago
   # (stock_data['Volume'].iloc[-1] * stock_data['Close'].iloc[-1] > 3000000) ## Volume (close * volume) greater than 3,000,000
)

    return conditions

def main():
    st.title('Qullamaggie + MM ADR Trend Scanner')

    with st.form(key='my_form'):
        start_date = st.date_input("Select start date", pd.to_datetime(one_year_ago))
        end_date = st.date_input("Select end date", datetime.now())
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        submit_button = st.form_submit_button("Submit")

    if submit_button and uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        input_file_name = os.path.splitext(uploaded_file.name)[0]
        total_tickers = len(df)
        progress_bar = st.progress(0)

        scanner_results_list = []
        for i, ticker in enumerate(df['Symbol'], start=1):
            try:
                data = yf.download(ticker, start=start_date, end=end_date)
                results = apply_scanner_conditions(data)
                if results.all():  # Check if any row (axis=1) has any True value
                    input_row = df[df['Symbol'] == ticker]
                    adr_value = input_row['ADR Value'].values[0]
                    adr_pct = input_row['ADR'].values[0]
                    rsi_value = input_row['RSI'].values[0]
                    scanner_results_list.append({'Ticker': ticker,
                                                'Close': round(data['Close'].iloc[-1], 2),
                                                'Volume': round(data['Volume'].iloc[-1], 2),
                                                'ADR Value': adr_value,
                                                'ADR PCT': adr_pct,
                                                'RSI': rsi_value,
                                                })
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
            
            progress_percent = int(i / total_tickers * 100)
            progress_bar.progress(progress_percent)

        scanner_results = pd.DataFrame(scanner_results_list)
        if not scanner_results.empty:
            st.subheader("Filtered Stocks")
            st.write(scanner_results[['Ticker', 'Close', 'Volume','ADR Value','ADR PCT','RSI']])
            output_file_name = f"QM_{input_file_name}.csv"
            scanner_results.to_csv(os.path.join(DATA_FOLDER, output_file_name), index=False)
            st.success(f"Results saved to {output_file_name}")
        else:
            st.write("No stocks found.")

if __name__ == "__main__":
    main()
