# import streamlit as st
# import yfinance as yf
# import pandas as pd
# import matplotlib.pyplot as plt
# import io
# import os
# from datetime import datetime, timedelta



# # Define the path to the data folder
# DATA_FOLDER = "./Data"

# # Function to calculate ADR Values
# def calculate_ADRV(data):
#     # Calculate the daily range (High - Low) using a lambda function
#     data['dr'] = data.apply(lambda x: x["High"] - x["Low"], axis=1)
    
#     # Calculate the average daily range (ADR) over a 20-period interval
#     data["adr"] = data['dr'].rolling(window=20).mean()
    
#     return data["adr"]

# # Function to calculate Average Daily Range (ADR) Percentage
# def calculate_ADR(data):
#     data['DailyHigh'] = data['High']
#     data['DailyLow'] = data['Low']
#     ADR_highlow = (data['DailyHigh'] / data['DailyLow']).rolling(window=20).mean()
#     ADR_perc = 100 * (ADR_highlow - 1)
#     return ADR_perc

# # Function to calculate Modified_ADR as absolute percentage change
# def calculate_modified_ADR(data):
#     data['dr_pct'] = data.apply(lambda x: 100 * (x["High"] / x["Low"] - 1), axis=1)
#     data["mod_adr"] = data['dr_pct'].rolling(window=20).mean()
#     return data["mod_adr"]

# # Function to calculate Relative Strength Index (RSI)
# def calculate_RSI(data, window=14):
#     delta = data['Close'].diff(1)
#     gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
#     loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
#     rs = gain / loss
#     rsi = 100 - (100 / (1 + rs))
#     return rsi


# def main():
#     st.title('ADR Scanner')

#     with st.form(key='my_form'):
#         # User input for start and end dates
#         start_date = st.date_input("Select start date", pd.to_datetime('2024-01-01'))
#         end_date = st.date_input("Select end date",  datetime.now())

#         # File selection
#         uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

#         # Submit button within the form
#         submit_button = st.form_submit_button("Submit")

#     if submit_button and uploaded_file is not None:
#         df = pd.read_csv(uploaded_file)

#         # Extract the input file name
#         input_file_name = os.path.splitext(uploaded_file.name)[0]
        
#         with st.spinner("Processing data..."):

#             # Calculate the total number of rows in the DataFrame
#             total_rows = len(df)
            
#             # Empty DataFrame to store results
#             plain_adr_results_list = []
    
#             for ticker in df['Symbol']:
#                 try:
#                     with st.spinner(f"Analysing {ticker}... ({i}/{total_rows})"):
#                         data = yf.download(ticker, start=start_date, end=end_date)
#                         adr_val = calculate_ADRV(data)
#                         adr = calculate_ADR(data)
#                         modified_adr = calculate_modified_ADR(data)
#                         rsi = calculate_RSI(data)
        
#                         # Check condition: ADR > 5
#                         if adr.iloc[-1] > 5:
#                             plain_adr_results_list.append({'Symbol': ticker,
#                                                            'Close': round(data['Close'].iloc[-1], 2),
#                                                            'Volume': round(data['Volume'].iloc[-1], 2),
#                                                            'ADR Value': round(adr_val.iloc[-1],2),
#                                                            'ADR %': round(adr.iloc[-1], 2),
#                                                            'Mod_ADR %': round(modified_adr.iloc[-1], 2),
#                                                            'RSI': round(rsi.iloc[-1], 2)})
#                 except Exception as e:
#                     print(f"Error processing {ticker}: {e}")

#         # Create DataFrame from results list
#         plain_adr_results_df = pd.DataFrame(plain_adr_results_list)

#         # Display the filtered stocks in a table
#         st.subheader('Filtered Stocks')
#         st.write(plain_adr_results_df)

#         # Save results to CSV with input file name
#         output_file_name = f"Plain_ADR_{input_file_name}.csv"
#         plain_adr_results_df.to_csv(os.path.join(DATA_FOLDER, output_file_name), index=False)
#         st.success(f"Results saved to {output_file_name}")
        




# if __name__ == "__main__":
#     main()


import streamlit as st
import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# Define the path to the data folder
DATA_FOLDER = "./Data"

# Function to calculate ADR Values
def calculate_ADRV(data):
    # Calculate the daily range (High - Low) using a lambda function
    data['dr'] = data.apply(lambda x: x["High"] - x["Low"], axis=1)
    
    # Calculate the average daily range (ADR) over a 20-period interval
    data["adr"] = data['dr'].rolling(window=20).mean()
    
    return data["adr"]

# Function to calculate Average Daily Range (ADR) Percentage
def calculate_ADR(data):
    data['DailyHigh'] = data['High']
    data['DailyLow'] = data['Low']
    ADR_highlow = (data['DailyHigh'] / data['DailyLow']).rolling(window=20).mean()
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

# Function to read stock symbols from a CSV file
def read_stock_symbols_from_csv(file):
    df = pd.read_csv(file)
    return df['Symbol'].tolist()

def main():
    st.title('ADR Scanner')

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

        # Calculate the total number of tickers
        total_tickers = len(df['Symbol'])
        progress_bar = st.progress(0)  # Initialize progress bar
        
        # Extract the input file name
        input_file_name = os.path.splitext(uploaded_file.name)[0]

        # Empty DataFrame to store results
        plain_adr_results_list = []
        
        for i, ticker in enumerate(df['Symbol'], start=1):
            try:
                with st.spinner(f"Analysing {ticker}... ({i}/{total_tickers})"):
                    data = yf.download(ticker, start=start_date, end=end_date)
                    adr_val = calculate_ADRV(data)
                    adr = calculate_ADR(data)
                    modified_adr = calculate_modified_ADR(data)
                    rsi = calculate_RSI(data)
    
                    # Check condition: ADR > 5
                    if adr.iloc[-1] > 5:
                        plain_adr_results_list.append({'Symbol': ticker,
                                                       'Close': round(data['Close'].iloc[-1], 2),
                                                       'Volume': round(data['Volume'].iloc[-1], 2),
                                                       'ADR Value': round(adr_val.iloc[-1],2),
                                                       'ADR': round(adr.iloc[-1], 2),
                                                       'Mod ADR': round(modified_adr.iloc[-1], 2),
                                                       'RSI': round(rsi.iloc[-1], 2)})
            except Exception as e:
                print(f"Error processing {ticker}: {e}")

            # Update progress bar
            progress_percent = int(i / total_tickers * 100)
            progress_bar.progress(progress_percent)
        
        # Create DataFrame from results list
        plain_adr_results_df = pd.DataFrame(plain_adr_results_list)

        # Display the filtered stocks in a table
        st.subheader('Filtered Stocks')
        st.write(plain_adr_results_df)

        # Save results to CSV with input file name
        output_file_name = f"Plain_ADR_{input_file_name}.csv"
        plain_adr_results_df.to_csv(os.path.join(DATA_FOLDER, output_file_name), index=False)
        st.success(f"Results saved to {output_file_name}")

if __name__ == "__main__":
    main()


