import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import plotly.graph_objects as go
import os

one_year_ago = datetime.now() - timedelta(days=365)


class StockAnalyzer:
    def __init__(self):
        pass

    def analyze_stocks(self, symbols_df, start_date, end_date, sma1, sma2, sma3, ema1, ema2,input_file_name):

        # Specify the path to the output folder
        output_folder = "./Data"

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        # Create a DataFrame for storing results
        results_df = pd.DataFrame(columns=['Stock Symbol', 'Close Price', f'SMA {sma1}', f'SMA {sma2}', f'SMA {sma3}', 
                                           f'EMA {ema1}', f'EMA {ema2}', 'SMA Crossover Percentage', 'EMA Crossover Percentage', 'Close vs SMA',
                                           'Declined Percentage', 'Positive Incline Percentage', '52 Week High', '52 Week Low'])

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

                    # Get 52-week high and low
                    high_52_week = historical_data['Close'].rolling(window=252).max().iloc[-1]
                    low_52_week = historical_data['Close'].rolling(window=252).min().iloc[-1]

                    # Format percentages with plus sign for positive values
                    sma_crossover_percentage_str = f"{'' if sma_crossover_percentage >= 0 else '-'}{abs(sma_crossover_percentage)}%"
                    ema_crossover_percentage_str = f"{'' if ema_crossover_percentage >= 0 else '-'}{abs(ema_crossover_percentage)}%"
                    declined_percentage_str = f"{'' if declined_percentage >= 0 else '-'}{abs(declined_percentage)}%"
                    positive_incline_percentage_str = f"{'' if positive_incline_percentage >= 0 else '-'}{abs(positive_incline_percentage)}%"

                    # Assuming 'results_df' is your existing DataFrame and 'row_data' is the dictionary containing the data for the new row
                    row_data = {
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
                        'Positive Incline Percentage': positive_incline_percentage_str,
                        '52 Week High': high_52_week,
                        '52 Week Low': low_52_week
                    }

                    # Convert the dictionary to a DataFrame and then concatenate it with the existing DataFrame
                    new_row_df = pd.DataFrame([row_data])
                    results_df = pd.concat([results_df, new_row_df], ignore_index=True)


            except Exception as e:
                st.write(f"Error analyzing {ticker_symbol}: {e}")

        # Save the output DataFrame to a CSV file with the same name as the input file
        file_name = os.path.join(output_folder, f"BNF_{input_file_name}")
        results_df.to_csv(file_name, index=False)

        return results_df

if __name__ == "__main__":
    st.title('Stock Analyzer')

    # User input widgets
    start_date = st.date_input("Select start date", one_year_ago)
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
            results = analyzer.analyze_stocks(symbols_df, start_date, end_date, sma1, sma2, sma3, ema1, ema2,uploaded_file.name)

            # # Save the output DataFrame to a CSV file
            results.to_csv("./Data/bnf_results.csv", index=False)
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

            # Create separate subplots for 52-week high and low stocks
            # Assuming 'results' DataFrame is correctly populated with '52 Week High' and '52 Week Low' columns

            # Create separate subplots for 52-week high and low stocks
            fig = go.Figure()

            # Plotting 52-week high
            fig.add_trace(go.Bar(x=results['Stock Symbol'], y=results['52 Week High'], name='52 Week High'))

            # Plotting 52-week low
            fig.add_trace(go.Bar(x=results['Stock Symbol'], y=results['52 Week Low'], name='52 Week Low'))

            # Update layout for grouped bar chart
            fig.update_layout(barmode='group', title='52 Week High and Low Stocks')

            # Display the plot in Streamlit
            st.plotly_chart(fig)
