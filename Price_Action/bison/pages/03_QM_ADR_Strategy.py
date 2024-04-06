# import streamlit as st
# import yfinance as yf
# import pandas as pd
# import os
# from datetime import datetime, timedelta

# # Define the path to the data folder
# DATA_FOLDER = "./Data"

# # Function to calculate Average Daily Range (ADR)
# @st.cache_data # Cache the data for 1 hour
# def calculate_ADR(data):
#     data['DailyHigh'] = data['High']
#     data['DailyLow'] = data['Low']
#     ADR_highlow = data['DailyHigh'] / data['DailyLow']
#     ADR_perc = ADR_highlow.rolling(window=14).apply(lambda x: (x.iloc[-1] / x.iloc[0]) - 1) * 100
#     return ADR_perc


# # Function to apply the scanner conditions
# @st.cache_data
# def apply_scanner_conditions(stock_data):
#     price_greater_than_1M = stock_data['Close'] > stock_data['Close'].shift(22) * 1.25
#     price_greater_than_3M = stock_data['Close'] > stock_data['Close'].shift(67) * 1.5
#     price_greater_than_6M = stock_data['Close'] > stock_data['Close'].shift(126) * 2.5
#     price_within_15_percent_of_high = stock_data['Close'] >= (stock_data['High'].rolling(window=6).max() * 0.85)
#     price_within_15_percent_of_low = stock_data['Close'] <= (stock_data['Low'].rolling(window=6).min() * 1.15)
#     stock_data['Dollar_Volume'] = stock_data['Close'] * stock_data['Volume']
#     volume_greater_than_3M = stock_data['Dollar_Volume'] > 1000000
#     scanner_results = price_greater_than_1M & price_greater_than_3M & \
#                       price_greater_than_6M & price_within_15_percent_of_high & \
#                       price_within_15_percent_of_low & volume_greater_than_3M
#     return scanner_results


# def main():
#     st.title('Qualamaggie ADR Strategy Scanner')

#     # Set end date as current date
#     end_date = datetime.today().date()

#     # Calculate start date as 6 months ago
#     start_date = end_date - timedelta(days=360)

#     # File selection
#     uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

#     # Submit button
#     if st.button('Submit') and uploaded_file is not None:
#         df = pd.read_csv(uploaded_file)
#         # Extract the input file name
#         input_file_name = os.path.splitext(uploaded_file.name)[0]

#         # Show a spinner while processing the data
#         with st.spinner("Processing data..."):
#             # Empty DataFrame to store results
#             scanner_results_list = []

#             for ticker in df['Symbol']:
#                 try:
#                     data = yf.download(ticker, start=start_date, end=end_date)
#                     adr = calculate_ADR(data)

#                     # Check if ADR is above 5
#                     #if adr.iloc[-1] > 5:
#                     results = apply_scanner_conditions(data)
#                     if results.any():
                        
#                         # Find the row in the input CSV file corresponding to the current ticker
#                         input_row = df[df['Symbol'] == ticker]
                    
#                         # Get the ADR and RSI values from the input row
#                         adr_value = input_row['ADR'].values[0]
#                         rsi_value = input_row['RSI'].values[0]
#                         scanner_results_list.append({'Ticker': ticker,
#                                                     'Close': round(data['Close'].iloc[-1], 2),
#                                                     'Volume': round(data['Volume'].iloc[-1], 2),
#                                                      'ADR': adr_value,  # Add ADR value from input CSV
#                                                     'RSI': rsi_value,  # Add RSI value from input CSV
#                                                     })

#                 except Exception as e:
#                     print(f"Error processing {ticker}: {e}")

#         # Create DataFrame from results list
#         scanner_results = pd.DataFrame(scanner_results_list)

#         if not scanner_results.empty:
#             # Displaying the results
#             st.subheader("Filtered Stocks")
#             st.write(scanner_results[['Ticker', 'Close', 'Volume']])

#             # Save results to CSV with input file name
#             output_file_name = f"QM_{input_file_name}.csv"
#             scanner_results.to_csv(os.path.join(DATA_FOLDER, output_file_name), index=False)
#             st.success(f"Results saved to {output_file_name}")
#         else:
#             st.write("No stocks found with ADR greater than 5.")

# if __name__ == "__main__":
#     main()

import streamlit as st
import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

# Define the path to the data folder
DATA_FOLDER = "./Data"

# Function to calculate Average Daily Range (ADR)
@st.cache_data # Cache the data for 1 hour
def calculate_ADR(data):
    data['DailyHigh'] = data['High']
    data['DailyLow'] = data['Low']
    ADR_highlow = data['DailyHigh'] / data['DailyLow']
    ADR_perc = ADR_highlow.rolling(window=14).apply(lambda x: (x.iloc[-1] / x.iloc[0]) - 1) * 100
    return ADR_perc

# Function to apply the scanner conditions
@st.cache_data
def apply_scanner_conditions(stock_data):
    price_greater_than_1M = stock_data['Close'] > stock_data['Close'].shift(22) * 1.25
    price_greater_than_3M = stock_data['Close'] > stock_data['Close'].shift(67) * 1.5
    price_greater_than_6M = stock_data['Close'] > stock_data['Close'].shift(126) * 2.5
    price_within_15_percent_of_high = stock_data['Close'] >= (stock_data['High'].rolling(window=6).max() * 0.85)
    price_within_15_percent_of_low = stock_data['Close'] <= (stock_data['Low'].rolling(window=6).min() * 1.15)
    stock_data['Dollar_Volume'] = stock_data['Close'] * stock_data['Volume']
    volume_greater_than_3M = stock_data['Dollar_Volume'] > 1000000
    scanner_results = price_greater_than_1M & price_greater_than_3M & \
                      price_greater_than_6M & price_within_15_percent_of_high & \
                      price_within_15_percent_of_low & volume_greater_than_3M
    return scanner_results

def main():
    st.title('Qualamaggie ADR Strategy Scanner')

    with st.form(key='my_form'):
        # User input for start and end dates
        start_date = st.date_input("Select start date", pd.to_datetime('2024-01-01'))
        end_date = st.date_input("Select end date", datetime.now())

        # File selection
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

        # Submit button within the form
        submit_button = st.form_submit_button("Submit")

    if submit_button and uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Extract the input file name
        input_file_name = os.path.splitext(uploaded_file.name)[0]

        # Calculate the total number of tickers
        total_tickers = len(df)
        progress_bar = st.progress(0)  # Initialize progress bar
        
        # Show a spinner while processing the data
        with st.spinner("Processing data..."):
            # Empty DataFrame to store results
            scanner_results_list = []

            for i, ticker in enumerate(df['Symbol'], start=1):
                try:
                    data = yf.download(ticker, start=start_date, end=end_date)
                    adr = calculate_ADR(data)

                    # Check if ADR is above 5
                    results = apply_scanner_conditions(data)
                    if results.any():
                        
                        # Find the row in the input CSV file corresponding to the current ticker
                        input_row = df[df['Symbol'] == ticker]
                    
                        # Get the ADR and RSI values from the input row
                        adr_value = input_row['ADR'].values[0]
                        rsi_value = input_row['RSI'].values[0]
                        scanner_results_list.append({'Ticker': ticker,
                                                    'Close': round(data['Close'].iloc[-1], 2),
                                                    'Volume': round(data['Volume'].iloc[-1], 2),
                                                     'ADR': adr_value,  # Add ADR value from input CSV
                                                    'RSI': rsi_value,  # Add RSI value from input CSV
                                                    })
                except Exception as e:
                    print(f"Error processing {ticker}: {e}")
                
                # Update progress bar
                progress_percent = int(i / total_tickers * 100)
                progress_bar.progress(progress_percent)

        # Create DataFrame from results list
        scanner_results = pd.DataFrame(scanner_results_list)

        if not scanner_results.empty:
            # Displaying the results
            st.subheader("Filtered Stocks")
            st.write(scanner_results[['Ticker', 'Close', 'Volume']])

            # Save results to CSV with input file name
            output_file_name = f"QM_{input_file_name}.csv"
            scanner_results.to_csv(os.path.join(DATA_FOLDER, output_file_name), index=False)
            st.success(f"Results saved to {output_file_name}")
        else:
            st.write("No stocks found with ADR greater than 5.")

if __name__ == "__main__":
    main()
