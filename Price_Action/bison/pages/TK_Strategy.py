# import streamlit as st
# import pandas as pd
# import yfinance as yf
# from datetime import datetime, timedelta
# import numpy as np

# class StockAnalyzer:
#     def __init__(self):
#         pass

#     def analyze_stocks(self, symbols_df, start_date, end_date, sma1, sma2, sma3, ema1, ema2):
#         # Create a DataFrame for storing results
#         results_df = pd.DataFrame(columns=['Stock Symbol', 'Close Price', f'SMA {sma1}', f'SMA {sma2}', f'SMA {sma3}', 
#                                            f'EMA {ema1}', f'EMA {ema2}', 'SMA Crossover Percentage', 'EMA Crossover Percentage', 'Close vs SMA',
#                                            'Declined Percentage', 'Positive Incline Percentage'])

#         for i, ticker_symbol in enumerate(symbols_df['Symbol'], start=1):
#             try:
#                 # Print progress and stock name
#                 st.write(f"Analyzing stock {i}/{len(symbols_df)}: {ticker_symbol}")

#                 # Create a Ticker object
#                 ticker = yf.Ticker(ticker_symbol)

#                 # Get the historical data for the stock within the specified date range
#                 historical_data = ticker.history(start=start_date, end=end_date)

#                 # Check if historical data is available for the specified date range
#                 if historical_data.empty:
#                     continue

#                 # Calculate the moving averages for the strategy
#                 historical_data[f'SMA {sma1}'] = historical_data['Close'].rolling(window=sma1).mean()
#                 historical_data[f'SMA {sma2}'] = historical_data['Close'].rolling(window=sma2).mean()
#                 historical_data[f'SMA {sma3}'] = historical_data['Close'].rolling(window=sma3).mean()
#                 historical_data[f'EMA {ema1}'] = historical_data['Close'].ewm(span=ema1, adjust=False).mean()
#                 historical_data[f'EMA {ema2}'] = historical_data['Close'].ewm(span=ema2, adjust=False).mean()

#                 # Check conditions for crossovers
#                 if (historical_data[f'SMA {sma2}'].iloc[-1] > historical_data[f'SMA {sma3}'].iloc[-1]) and \
#                    (historical_data[f'SMA {sma2}'].iloc[-1] > historical_data[f'SMA {sma1}'].iloc[-1]):
#                     # Calculate the percentage difference for SMA crossover
#                     sma_crossover_percentage = ((historical_data[f'SMA {sma2}'].iloc[-1] - historical_data[f'SMA {sma3}'].iloc[-1]) /
#                                                 historical_data[f'SMA {sma3}'].iloc[-1]) * 100

#                     # Calculate the percentage difference for EMA crossover
#                     ema_crossover_percentage = ((historical_data[f'EMA {ema1}'].iloc[-1] - historical_data[f'EMA {ema2}'].iloc[-1]) /
#                                                 historical_data[f'EMA {ema2}'].iloc[-1]) * 100

#                     # Determine if the close price is below or above the crossover
#                     close_vs_sma = 'Negative' if historical_data['Close'].iloc[-1] < historical_data[f'SMA {sma2}'].iloc[-1] else 'Positive'

#                     # Calculate Declined Percentage and Positive Incline Percentage
#                     declined_percentage = ((historical_data[f'SMA {sma2}'].iloc[-1] - historical_data['Close'].iloc[-1]) /
#                                            historical_data[f'SMA {sma2}'].iloc[-1]) * 100
#                     positive_incline_percentage = ((historical_data['Close'].iloc[-1] - historical_data[f'SMA {sma2}'].iloc[-1]) /
#                                                  historical_data[f'SMA {sma2}'].iloc[-1]) * 100

#                     # Format percentages with plus sign for positive values
#                     sma_crossover_percentage_str = f"{'' if sma_crossover_percentage >= 0 else '-'}{abs(sma_crossover_percentage)}%"
#                     ema_crossover_percentage_str = f"{'' if ema_crossover_percentage >= 0 else '-'}{abs(ema_crossover_percentage)}%"
#                     declined_percentage_str = f"{'' if declined_percentage >= 0 else '-'}{abs(declined_percentage)}%"
#                     positive_incline_percentage_str = f"{'' if positive_incline_percentage >= 0 else '-'}{abs(positive_incline_percentage)}%"

#                     # Append the results to the DataFrame
#                     results_df = results_df.append({
#                         'Stock Symbol': ticker_symbol,
#                         'Close Price': historical_data['Close'].iloc[-1],
#                         f'SMA {sma1}': historical_data[f'SMA {sma1}'].iloc[-1],
#                         f'SMA {sma2}': historical_data[f'SMA {sma2}'].iloc[-1],
#                         f'SMA {sma3}': historical_data[f'SMA {sma3}'].iloc[-1],
#                         f'EMA {ema1}': historical_data[f'EMA {ema1}'].iloc[-1],
#                         f'EMA {ema2}': historical_data[f'EMA {ema2}'].iloc[-1],
#                         'SMA Crossover Percentage': sma_crossover_percentage_str,
#                         'EMA Crossover Percentage': ema_crossover_percentage_str,
#                         'Close vs SMA': close_vs_sma,
#                         'Declined Percentage': declined_percentage_str,
#                         'Positive Incline Percentage': positive_incline_percentage_str
#                     }, ignore_index=True)

#             except Exception as e:
#                 st.write(f"Error analyzing {ticker_symbol}: {e}")

#         return results_df

# if __name__ == "__main__":
#     st.title('Stock Analyzer')

#     # User input widgets
#     start_date = st.date_input("Select start date", datetime.now() - timedelta(days=365))
#     end_date = st.date_input("Select end date", datetime.now())
#     uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

#     if uploaded_file is not None:
#         symbols_df = pd.read_csv(uploaded_file)

#         sma1 = st.slider('Select SMA 1', min_value=1, max_value=100, value=25)
#         sma2 = st.slider('Select SMA 2', min_value=1, max_value=100, value=44)
#         sma3 = st.slider('Select SMA 3', min_value=1, max_value=100, value=200)
#         ema1 = st.slider('Select EMA 1', min_value=1, max_value=100, value=44)
#         ema2 = st.slider('Select EMA 2', min_value=1, max_value=100, value=200)

#         if st.button('Submit'):
#             analyzer = StockAnalyzer()
#             results = analyzer.analyze_stocks(symbols_df, start_date, end_date, sma1, sma2, sma3, ema1, ema2)

#             # Save the output DataFrame to a CSV file
#             results.to_csv("results.csv", index=False)
#             st.success("Results saved to results.csv")

#             # Split the results into two DataFrames based on 'Close vs SMA'
#             positive_results = results[results['Close vs SMA'] == 'Positive']
#             negative_results = results[results['Close vs SMA'] == 'Negative']

#             # Display the positive results table
#             st.subheader("Positive Results")
#             st.dataframe(positive_results)

#             # Display the negative results table
#             st.subheader("Negative Results")
#             st.dataframe(negative_results)


import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import plotly.graph_objects as go

class StockAnalyzer:
    def __init__(self):
        pass

    def analyze_stocks(self, symbols_df, start_date, end_date, sma1, sma2, sma3, ema1, ema2):
        # Create a DataFrame for storing results
        results_df = pd.DataFrame(columns=['Stock Symbol', 'Close Price', f'SMA {sma1}', f'SMA {sma2}', f'SMA {sma3}', 
                                           f'EMA {ema1}', f'EMA {ema2}', 'SMA Crossover Percentage', 'EMA Crossover Percentage', 'Close vs SMA',
                                           'Declined Percentage', 'Positive Incline Percentage'])

        for i, ticker_symbol in enumerate(symbols_df['Symbol'], start=1):
            try:
                # Print progress and stock name
                st.write(f"Analyzing stock {i}/{len(symbols_df)}: {ticker_symbol}")

                # Create a Ticker object
                ticker = yf.Ticker(ticker_symbol)

                # Get the historical data for the stock within the specified date range
                historical_data = ticker.history(start=start_date, end=end_date)

                # Check if historical data is available for the specified date range
                if historical_data.empty:
                    continue

                # Calculate the moving averages for the strategy
                historical_data[f'SMA {sma1}'] = historical_data['Close'].rolling(window=sma1).mean()
                historical_data[f'SMA {sma2}'] = historical_data['Close'].rolling(window=sma2).mean()
                historical_data[f'SMA {sma3}'] = historical_data['Close'].rolling(window=sma3).mean()
                historical_data[f'EMA {ema1}'] = historical_data['Close'].ewm(span=ema1, adjust=False).mean()
                historical_data[f'EMA {ema2}'] = historical_data['Close'].ewm(span=ema2, adjust=False).mean()

                # Check conditions for crossovers
                if (historical_data[f'SMA {sma2}'].iloc[-1] > historical_data[f'SMA {sma3}'].iloc[-1]) and \
                   (historical_data[f'SMA {sma2}'].iloc[-1] > historical_data[f'SMA {sma1}'].iloc[-1]):
                    # Calculate the percentage difference for SMA crossover
                    sma_crossover_percentage = ((historical_data[f'SMA {sma2}'].iloc[-1] - historical_data[f'SMA {sma3}'].iloc[-1]) /
                                                historical_data[f'SMA {sma3}'].iloc[-1]) * 100

                    # Calculate the percentage difference for EMA crossover
                    ema_crossover_percentage = ((historical_data[f'EMA {ema1}'].iloc[-1] - historical_data[f'EMA {ema2}'].iloc[-1]) /
                                                historical_data[f'EMA {ema2}'].iloc[-1]) * 100

                    # Determine if the close price is below or above the crossover
                    close_vs_sma = 'Negative' if historical_data['Close'].iloc[-1] < historical_data[f'SMA {sma2}'].iloc[-1] else 'Positive'

                    # Calculate Declined Percentage and Positive Incline Percentage
                    declined_percentage = ((historical_data[f'SMA {sma2}'].iloc[-1] - historical_data['Close'].iloc[-1]) /
                                           historical_data[f'SMA {sma2}'].iloc[-1]) * 100
                    positive_incline_percentage = ((historical_data['Close'].iloc[-1] - historical_data[f'SMA {sma2}'].iloc[-1]) /
                                                 historical_data[f'SMA {sma2}'].iloc[-1]) * 100

                    # Format percentages with plus sign for positive values
                    sma_crossover_percentage_str = f"{'' if sma_crossover_percentage >= 0 else '-'}{abs(sma_crossover_percentage)}%"
                    ema_crossover_percentage_str = f"{'' if ema_crossover_percentage >= 0 else '-'}{abs(ema_crossover_percentage)}%"
                    declined_percentage_str = f"{'' if declined_percentage >= 0 else '-'}{abs(declined_percentage)}%"
                    positive_incline_percentage_str = f"{'' if positive_incline_percentage >= 0 else '-'}{abs(positive_incline_percentage)}%"

                    # Append the results to the DataFrame
                    results_df = results_df.append({
                        'Stock Symbol': ticker_symbol,
                        'Close Price': historical_data['Close'].iloc[-1],
                        f'SMA {sma1}': historical_data[f'SMA {sma1}'].iloc[-1],
                        f'SMA {sma2}': historical_data[f'SMA {sma2}'].iloc[-1],
                        f'SMA {sma3}': historical_data[f'SMA {sma3}'].iloc[-1],
                        f'EMA {ema1}': historical_data[f'EMA {ema1}'].iloc[-1],
                        f'EMA {ema2}': historical_data[f'EMA {ema2}'].iloc[-1],
                        'SMA Crossover Percentage': sma_crossover_percentage_str,
                        'EMA Crossover Percentage': ema_crossover_percentage_str,
                        'Close vs SMA': close_vs_sma,
                        'Declined Percentage': declined_percentage_str,
                        'Positive Incline Percentage': positive_incline_percentage_str
                    }, ignore_index=True)

            except Exception as e:
                st.write(f"Error analyzing {ticker_symbol}: {e}")

        return results_df

if __name__ == "__main__":
    st.title('Stock Analyzer')

    # User input widgets
    start_date = st.date_input("Select start date", datetime.now() - timedelta(days=365))
    end_date = st.date_input("Select end date", datetime.now())
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        symbols_df = pd.read_csv(uploaded_file)

        sma1 = st.slider('Select SMA 1', min_value=1, max_value=100, value=25)
        sma2 = st.slider('Select SMA 2', min_value=1, max_value=100, value=44)
        sma3 = st.slider('Select SMA 3', min_value=1, max_value=100, value=200)
        ema1 = st.slider('Select EMA 1', min_value=1, max_value=100, value=44)
        ema2 = st.slider('Select EMA 2', min_value=1, max_value=100, value=200)

        if st.button('Submit'):
            analyzer = StockAnalyzer()
            results = analyzer.analyze_stocks(symbols_df, start_date, end_date, sma1, sma2, sma3, ema1, ema2)

            # Save the output DataFrame to a CSV file
            results.to_csv("results.csv", index=False)
            st.success("Results saved to results.csv")

            # Convert 'Positive Incline Percentage' to numeric
            results['Positive Incline Percentage'] = pd.to_numeric(results['Positive Incline Percentage'].str.rstrip('%'), errors='coerce')

            # Filter positive incline percentages
            positive_incline_df = results[results['Positive Incline Percentage'] >= 0]
            negative_incline_df = results[results['Positive Incline Percentage'] < 0]

            # Plotting symbols with positive incline percentage in green
            fig = go.Figure(data=[go.Bar(x=positive_incline_df['Stock Symbol'], y=positive_incline_df['Positive Incline Percentage'],
                                         marker_color='green')])
            fig.update_layout(title='Stocks with Positive Incline Percentage', xaxis_tickangle=45)
            st.plotly_chart(fig)

            # Plotting symbols with negative incline percentage in red
            fig = go.Figure(data=[go.Bar(x=negative_incline_df['Stock Symbol'], y=negative_incline_df['Positive Incline Percentage'],
                                         marker_color='red')])
            fig.update_layout(title='Stocks with Negative Incline Percentage', xaxis_tickangle=45)
            st.plotly_chart(fig)

