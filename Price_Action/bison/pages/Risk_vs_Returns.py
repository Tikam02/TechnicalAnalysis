import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt

# Setting stock symbols and time range
def get_stock_data(symbols):
    start = dt.date.today() - dt.timedelta(days=365 * 3)
    end = dt.date.today()

    # Downloading and processing stock data
    df = pd.DataFrame()
    for symbol in symbols:
        df[symbol] = yf.download(symbol, start=start, end=end)['Adj Close']

    # Dropping rows with missing values
    df = df.dropna()

    return df

# Calculating percentage change in stock prices
def calculate_returns(df):
    rets = df.pct_change(periods=3)
    return rets

# Plotting functions
def plot_scatter_matrix(rets):
    fig, axes = plt.subplots(nrows=len(rets.columns), ncols=len(rets.columns), figsize=(10, 10))
    pd.plotting.scatter_matrix(rets, diagonal='kde', ax=axes, figsize=(10, 10))
    st.pyplot(fig)

def plot_correlation_heatmap(rets):
    corr = rets.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(corr, cmap='Blues', interpolation='none')
    ax.set_title("Correlation Matrix Heatmap")
    ax.set_xticks(range(len(corr)))
    ax.set_yticks(range(len(corr)))
    ax.set_xticklabels(corr.columns)
    ax.set_yticklabels(corr.columns)
    st.pyplot(fig)

def plot_risk_returns(rets):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(rets.columns, rets.std(), color='red', alpha=0.6, label='Risk (Std. Dev.)')
    ax.bar(rets.columns, rets.mean(), color='blue', alpha=0.6, label='Average Returns')
    ax.set_title("Risk and Average Returns")
    ax.set_xlabel("Stock Symbols")
    ax.set_ylabel("Value")
    ax.legend()
    st.pyplot(fig)

def plot_stacked_risk_returns(rets, symbols):
    fig, ax = plt.subplots(figsize=(10, 4))
    width = 0.35
    ind = np.arange(len(symbols))
    ax.bar(ind, rets.mean(), width, color='blue', label='Average of Returns')
    ax.bar(ind, rets.std(), width, bottom=rets.mean(), color='red', label='Risk of Returns')
    ax.set_ylabel('Value')
    ax.set_xlabel('Stock Symbols')
    ax.set_title('Risk vs Average Returns')
    ax.set_xticks(ind)
    ax.set_xticklabels(symbols)
    ax.legend()
    st.pyplot(fig)

def plot_expected_returns_risk(rets):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(rets.mean(), rets.std())
    ax.set_xlabel('Expected Returns')
    ax.set_ylabel('Risk')
    for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
        ax.annotate(label, xy=(x, y), xytext=(5, 5), textcoords='offset points')
    ax.set_title('Risk vs Expected Returns')
    st.pyplot(fig)

def display_risk_returns_table(rets):
    risk_returns_table = pd.DataFrame({'Risk': rets.std(), 'Expected Returns': rets.mean()})
    st.write("Table: Risk vs Expected Returns")
    st.write(risk_returns_table)

# Streamlit app
st.title("Risk Vs Returns Analysis")

# User input for stock symbols
stock_symbols = st.text_input("Enter stock symbols (comma-separated)", value="BCLIND.NS, HSCL.NS, GPPL.NS, FCL.NS, HDFCBANK.NS")
if st.button('Submit'):
    symbols = [symbol.strip() for symbol in stock_symbols.split(",")]
    
    # Get stock data
    stock_data = get_stock_data(symbols)
    
    # Calculate returns
    returns = calculate_returns(stock_data)
    
    # Plot visualizations
    st.subheader("Scatter Matrix")
    plot_scatter_matrix(returns)
    
    st.subheader("Correlation Matrix Heatmap")
    plot_correlation_heatmap(returns)
    
    st.subheader("Risk and Average Returns")
    plot_risk_returns(returns)
    
    st.subheader("Stacked Bar Chart: Risk vs Average Returns")
    plot_stacked_risk_returns(returns, symbols)
    
    st.subheader("Scatter Plot: Expected Returns vs Risk")
    plot_expected_returns_risk(returns)
    
    st.subheader("Risk vs Expected Returns Table")
    display_risk_returns_table(returns)
