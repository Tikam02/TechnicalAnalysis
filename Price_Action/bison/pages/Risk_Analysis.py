import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import os
import matplotlib.pyplot as plt


def process_stock_symbols(selected_symbols):
    # Initialize an empty DataFrame
    stocks_data = pd.DataFrame()

    # Download stock data using yfinance and concatenate into a single DataFrame
    for symbol in selected_symbols:
        stock = yf.Ticker(symbol)
        data = stock.history(period="max")
        data['Symbol'] = symbol  # Add a column to identify the stock
        stocks_data = pd.concat([stocks_data, data])

    # Reset the index
    stocks_data.reset_index(inplace=True)

    # Convert the 'Date' column to datetime format
    stocks_data['Date'] = pd.to_datetime(stocks_data['Date'])

    # Pivot the DataFrame
    pivot_data = stocks_data.pivot(index='Date', columns='Symbol', values='Close')

    # Time Series Analysis
    fig1 = make_subplots(rows=1, cols=1)
    for column in pivot_data.columns:
        fig1.add_trace(go.Scatter(x=pivot_data.index, y=pivot_data[column], name=column), row=1, col=1)
    fig1.update_layout(title_text='Time Series of Closing Prices', xaxis_title='Date', yaxis_title='Closing Price', legend_title='Ticker', showlegend=True)

    # Volatility Analysis
    volatility = pivot_data.std().sort_values(ascending=False)
    fig2 = px.bar(volatility, x=volatility.index, y=volatility.values, labels={'y': 'Standard Deviation', 'x': 'Ticker'}, title='Volatility of Closing Prices (Standard Deviation)')

    # Risk and Return Analysis
    daily_returns = pivot_data.pct_change().dropna()
    avg_daily_return = daily_returns.mean()
    risk = daily_returns.std()
    risk_return_df = pd.DataFrame({'Risk': risk, 'Average Daily Return': avg_daily_return})

    # Update the risk and average daily return percentages to 2 decimal places
    risk_return_df_percentage_rounded = risk_return_df * 100
    risk_return_df_percentage_rounded = risk_return_df_percentage_rounded.round(2)

    # Create table with rounded percentages
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=["Ticker", "Risk (%)", "Average Daily Return (%)"],
                    fill_color='paleturquoise',
                    align='center'),
        cells=dict(values=[risk_return_df_percentage_rounded.index, risk_return_df_percentage_rounded['Risk'], risk_return_df_percentage_rounded['Average Daily Return']],
                   fill_color='lavender',
                   align='center')
    )])

    # Update layout for table
    table_fig.update_layout(
        title='Risk vs. Return Analysis (Percentages)',
        showlegend=False,
        height=400
    )

    # Show all plots in one page
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

    # Display the risk vs return table
    st.subheader('Risk vs. Return Analysis Table')
    st.write(risk_return_df_percentage_rounded)

    # Stacked bar chart for risk vs return
    plt.figure(figsize=(10, 4))
    width = 0.35
    ind = range(len(selected_symbols))
    for i, symbol in enumerate(selected_symbols):
        plt.bar(ind[i], avg_daily_return[symbol], width, color='blue', label='Average Daily Return' if i == 0 else "")
        plt.bar(ind[i], risk[symbol], width, bottom=avg_daily_return[symbol], color='red', label='Risk' if i == 0 else "")
    plt.ylabel('Value')
    plt.xlabel('Stock Symbols')
    plt.title('Risk vs Average Returns')
    plt.xticks(ind, selected_symbols)
    plt.legend()
    st.pyplot(plt)

    # Scatter plot for risk vs return
    scatter_fig = px.scatter(risk_return_df, x='Risk', y='Average Daily Return', text=risk_return_df.index, title='Risk vs. Return Analysis')
    scatter_fig.update_traces(textposition='top center', marker=dict(size=10))
    st.plotly_chart(scatter_fig)

# Define the path to the CSV file
csv_file_path = os.path.join("Data", "watchlist.csv")

# Check if the CSV file exists
if not os.path.exists(csv_file_path):
    st.error("CSV file 'watchlist.csv' not found in the 'Data' directory.")
    st.stop()

# Read the CSV file
watchlist_df = pd.read_csv(csv_file_path)

# Get the list of stock symbols from the CSV file
stock_symbols = watchlist_df['Symbol'].tolist()

# If no symbols are available, show a message and stop execution
if not stock_symbols:
    st.error("No stock symbols found in the CSV file.")
    st.stop()

# Let the user select stock symbols
selected_symbols = st.multiselect("Select Stock Symbols", stock_symbols)

# If no symbols are selected, show a message and stop execution
if not selected_symbols:
    st.error("Please select at least one stock symbol.")
    st.stop()

# Add a submit button to trigger processing
if st.button("Submit"):
    # Call the main processing function
    process_stock_symbols(selected_symbols)
