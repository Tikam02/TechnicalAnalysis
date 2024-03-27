import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Function to fetch stock data
def get_stock_data(stock_name, start_date, end_date):
    stock = yf.Ticker(stock_name)
    return stock.history(start=start_date, end=end_date)

# Function to display stock price chart using Plotly
def display_stock_chart(stock_name, start_date, end_date):
    stock_data = get_stock_data(stock_name, start_date, end_date)
    if not stock_data.empty:
        fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                             open=stock_data['Open'],
                                             high=stock_data['High'],
                                             low=stock_data['Low'],
                                             close=stock_data['Close'])])
        fig.update_layout(title=f"{stock_name} Candlestick Chart (Last 30 Days)",
                          xaxis_title="Date",
                          yaxis_title="Price")
        st.plotly_chart(fig)

# Main function
def main():
    st.title('TSA Capital and Research')

    # Calculate start and end dates for the last 30 days
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')

    # Show stock price chart for the last 30 days
    display_stock_chart("^NSEI", start_date, end_date)

    # Calculate RSI using pandas_ta
    data = get_stock_data("^NSEI", start_date, end_date)
    data['RSI'] = ta.rsi(data['Close'], length=14)
    latest_rsi = data['RSI'].iloc[-1]

    # Gauge chart setup
    plot_bgcolor = "#def"
    quadrant_colors = [plot_bgcolor, "#f25829", "#f2a529", "#eff229", "#85e043", "#2bad4e"]
    quadrant_text = ["", "<b>Extreme Overbought</b>", "<b>Momentum Zone</b>", "<b>Neutral</b>",
                     "<b>Over Sold</b>", "<b>Extremely Oversold</b>"]
    n_quadrants = len(quadrant_colors) - 1

    min_value = 0
    max_value = 100
    hand_length = np.sqrt(2) / 4
    hand_angle = 360 * (-latest_rsi / 2 - min_value) / (max_value - min_value) - 180

    # Create gauge chart
    gauge_fig = go.Figure(
        data=[go.Pie(values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                     rotation=90,
                     hole=0.5,
                     marker_colors=quadrant_colors,
                     text=quadrant_text,
                     textinfo="text",
                     hoverinfo="skip",
                     sort=False)],
        layout=go.Layout(showlegend=False,
                         margin=dict(b=0, t=10, l=10, r=10),
                         width=800,
                         height=600,
                         paper_bgcolor=plot_bgcolor,
                         annotations=[go.layout.Annotation(
                             text=f"<b>Nifty RSI Level:</b><br>{latest_rsi:.2f}",
                             x=0.5, xanchor="center", xref="paper",
                             y=0.25, yanchor="bottom", yref="paper",
                             showarrow=False,
                             font=dict(size=14))],
                         shapes=[go.layout.Shape(type="circle", x0=0.48, x1=0.52, y0=0.48, y1=0.52,
                                                 fillcolor="#333", line_color="#333"),
                                 go.layout.Shape(type="line", x0=0.5, x1=0.5 + hand_length * np.cos(np.radians(hand_angle)),
                                                 y0=0.5, y1=0.5 + hand_length * np.sin(np.radians(hand_angle)),
                                                 line=dict(color="#333", width=5))])
    )
    st.plotly_chart(gauge_fig)

if __name__ == "__main__":
    main()
