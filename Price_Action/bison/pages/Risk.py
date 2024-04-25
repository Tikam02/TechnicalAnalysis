# import streamlit as st
# import riskfolio as rp
# import numpy as np
# import pandas as pd
# import yfinance as yf
# import warnings
# import matplotlib.pyplot as plt

# warnings.filterwarnings("ignore")
# pd.options.display.float_format = '{:.4%}'.format

# # Date range
# start = '2022-01-01'
# end = '2024-04-22'

# # Read assets from CSV file
# assets_df = pd.read_csv('./Data/Plain_ADR_niftytotal750.csv')
# assets = assets_df['Symbol'].tolist()
# assets.sort()

# # Downloading data
# data = yf.download(assets, start=start, end=end)
# data = data.loc[:, ('Adj Close', slice(None))]
# data.columns = assets

# # Calculating returns
# Y = data[assets].pct_change().dropna()

# # Building the portfolio object
# port = rp.Portfolio(returns=Y)

# # Calculating optimal portfolio
# method_mu='hist' # Method to estimate expected returns based on historical data.
# method_cov='hist' # Method to estimate covariance matrix based on historical data.
# port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)
# model='Classic' # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
# obj = 'Sharpe' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
# hist = True # Use historical scenarios for risk measures that depend on scenarios
# rf = 0 # Risk free rate
# l = 0 # Risk aversion factor, only useful when obj is 'Utility'

# # Risk Measures available
# rms = ['MV', 'MAD', 'MSV', 'FLPM', 'SLPM', 'CVaR', 'EVaR', 'WR', 'MDD', 'ADD', 'CDaR', 'UCI', 'EDaR']

# rm = 'CVaR' # Risk measure
# w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)


# # Plotting the composition of the portfolio for the optimal risk measure
# def plot_portfolio_pie(weights, title, cmap="tab20", height=6, width=10):
#     ax = rp.plot_pie(w=weights, title=title, others=0.05, nrow=25, cmap=cmap,
#                      height=height, width=width, ax=None)
#     st.pyplot(ax.figure)


# # Call the function to plot the pie chart
# plot_portfolio_pie(weights=w, title='Sharpe Mean Variance', cmap="tab20", height=6, width=10)


# # Plotting the composition of the portfolio for different risk measures
# w_cvar = port.optimization(model=model, rm='CVaR', obj=obj, rf=rf, l=l, hist=hist)
# plot_portfolio_pie(weights=w_cvar, title='Sharpe Mean CVaR', cmap="tab20", height=6, width=10)

# # Plotting the weights across different risk measures as a bar plot
# def plot_portfolio_bar(weights_df):
#     fig, ax = plt.subplots(figsize=(14, 6))
#     weights_df.plot.bar(ax=ax)
#     st.pyplot(fig)

# # Generating DataFrame containing the portfolio weights for different risk measures
# w_s = pd.DataFrame([])
# for rm in rms:
#     w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)
#     w_s = pd.concat([w_s, w], axis=1)
# w_s.columns = rms

# # Plotting the weights across different risk measures as a bar plot
# plot_portfolio_bar(weights_df=w_s)

# # Displaying the table of portfolio weights for different risk measures
# st.write("Optimized Weights for Each Risk Measure:")
# st.dataframe(w_s.style.format("{:.2%}").background_gradient(cmap='YlGn'))

# # Adding the efficient frontier graph
# points = 50 # Number of points of the frontier
# rm = 'CVaR' # Specify the risk measure for the efficient frontier

# frontier = port.efficient_frontier(model=model, rm=rm, points=points, rf=rf, hist=hist)

# # Displaying the last few points of the frontier
# st.write("Efficient Frontier Points:")
# #st.dataframe(frontier.T.head())

# label = 'Max Risk Adjusted Return Portfolio' # Title of point
# mu = port.mu # Expected returns
# cov = port.cov # Covariance matrix
# returns = port.returns # Returns of the assets

# ax = rp.plot_frontier(w_frontier=frontier, mu=mu, cov=cov, returns=returns, rm=rm,
#                       rf=rf, alpha=0.05, cmap='viridis', w=w_cvar, label=label,
#                       marker='*', s=16, c='r', height=6, width=10, ax=None)
# st.pyplot(ax.figure)


import streamlit as st
import riskfolio as rp
import numpy as np
import pandas as pd
import yfinance as yf
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
pd.options.display.float_format = '{:.4%}'.format

# User inputs for start and end dates
start_date = st.date_input("Start Date", pd.to_datetime('2022-01-01'))
end_date = st.date_input("End Date", pd.to_datetime('2024-04-22'))

# User uploads the CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    assets_df = pd.read_csv(uploaded_file)
    assets = assets_df['Symbol'].tolist()
    assets.sort()

    # Downloading data
    data = yf.download(assets, start=start_date, end=end_date)
    data = data.loc[:, ('Adj Close', slice(None))]
    data.columns = assets

    # Calculating returns
    Y = data[assets].pct_change().dropna()

    # Building the portfolio object
    port = rp.Portfolio(returns=Y)

    # Calculating optimal portfolio
    method_mu='hist' # Method to estimate expected returns based on historical data.
    method_cov='hist' # Method to estimate covariance matrix based on historical data.
    port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)
    model='Classic' # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
    obj = 'Sharpe' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
    hist = True # Use historical scenarios for risk measures that depend on scenarios
    rf = 0 # Risk free rate
    l = 0 # Risk aversion factor, only useful when obj is 'Utility'

    # Risk Measures available
    rms = ['MV', 'MAD', 'MSV', 'FLPM', 'SLPM', 'CVaR', 'EVaR', 'WR', 'MDD', 'ADD', 'CDaR', 'UCI', 'EDaR']

    rm = 'CVaR' # Risk measure
    w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)

    # Plotting the composition of the portfolio for the optimal risk measure
    def plot_portfolio_pie(weights, title, cmap="tab20", height=6, width=10):
        ax = rp.plot_pie(w=weights, title=title, others=0.05, nrow=25, cmap=cmap,
                         height=height, width=width, ax=None)
        st.pyplot(ax.figure)

    # Call the function to plot the pie chart
    plot_portfolio_pie(weights=w, title='Sharpe Mean Variance', cmap="tab20", height=6, width=10)

    # Plotting the composition of the portfolio for different risk measures
    w_cvar = port.optimization(model=model, rm='CVaR', obj=obj, rf=rf, l=l, hist=hist)
    plot_portfolio_pie(weights=w_cvar, title='Sharpe Mean CVaR', cmap="tab20", height=6, width=10)

    # Plotting the weights across different risk measures as a bar plot
    def plot_portfolio_bar(weights_df):
        fig, ax = plt.subplots(figsize=(14, 6))
        weights_df.plot.bar(ax=ax)
        st.pyplot(fig)

    # Generating DataFrame containing the portfolio weights for different risk measures
    w_s = pd.DataFrame([])
    for rm in rms:
        w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)
        w_s = pd.concat([w_s, w], axis=1)
    w_s.columns = rms

    # Plotting the weights across different risk measures as a bar plot
    plot_portfolio_bar(weights_df=w_s)

    # Displaying the table of portfolio weights for different risk measures
    st.write("Optimized Weights for Each Risk Measure:")
    st.dataframe(w_s.style.format("{:.2%}").background_gradient(cmap='YlGn'))

    # Adding the efficient frontier graph
    points = 50 # Number of points of the frontier
    rm = 'CVaR' # Specify the risk measure for the efficient frontier

    frontier = port.efficient_frontier(model=model, rm=rm, points=points, rf=rf, hist=hist)

    # Displaying the last few points of the frontier
    st.write("Efficient Frontier Points:")
    #st.dataframe(frontier.T.head())

    label = 'Max Risk Adjusted Return Portfolio' # Title of point
    mu = port.mu # Expected returns
    cov = port.cov # Covariance matrix
    returns = port.returns # Returns of the assets

    ax = rp.plot_frontier(w_frontier=frontier, mu=mu, cov=cov, returns=returns, rm=rm,
                          rf=rf, alpha=0.05, cmap='viridis', w=w_cvar, label=label,
                          marker='*', s=16, c='r', height=6, width=10, ax=None)
    st.pyplot(ax.figure)
