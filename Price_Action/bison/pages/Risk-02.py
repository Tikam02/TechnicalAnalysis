import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

# Define the list of stock symbols
stock_symbols = ['EMUDHRA.NS', 'AEGISCHEM.NS', 'SANGHVIMOV.NS', 'SHILPAMED.NS', 'TORNTPOWER.NS', 'COCHINSHIP.NS']

# Initialize an empty DataFrame
stocks_data = pd.DataFrame()

# Download stock data using yfinance and concatenate into a single DataFrame
for symbol in stock_symbols:
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
scatter_fig = px.scatter(risk_return_df, x='Risk', y='Average Daily Return', text=risk_return_df.index, title='Risk vs. Return Analysis')
scatter_fig.update_traces(textposition='top center', marker=dict(size=10))

# Stacked bar chart for risk vs return
plt.figure(figsize=(10, 4))
width = 0.35
ind = np.arange(len(stock_symbols))
for i, symbol in enumerate(stock_symbols):
    plt.bar(ind[i], avg_daily_return[symbol], width, color='blue', label='Average Daily Return' if i == 0 else "")
    plt.bar(ind[i], risk[symbol], width, bottom=avg_daily_return[symbol], color='red', label='Risk' if i == 0 else "")
plt.ylabel('Value')
plt.xlabel('Stock Symbols')
plt.title('Risk vs Average Returns')
plt.xticks(ind, stock_symbols)
plt.legend()

# Show all plots in one page
st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(scatter_fig)
st.pyplot(plt)  # Pass the plt object to st.pyplot()

# Display the risk-return table
st.subheader('Risk vs. Return Analysis Table')
st.write(risk_return_df)
