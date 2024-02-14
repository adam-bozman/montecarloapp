import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page layout
st.set_page_config(page_title='Monte Carlo', layout='wide', initial_sidebar_state='expanded',
                   menu_items={
                       'Get Help': 'https://github.com/adam-bozman/montecarloapp',
                       'About': "https://www.adambozman.com/"
                   })

st.title('Stock Price Forecasting with Monte Carlo Simulations')

# Header image
st.image('img/header.png', use_column_width=True)

# Sidebar parameters
forecast_length = st.sidebar.slider('Select Forecast Length (Days):', min_value=30, max_value=365, value=252, step=1)
view_full_forecast = st.sidebar.checkbox('View Entire Forecast')
num_runs = st.sidebar.slider('Number of Simulation Runs:', min_value=100, max_value=5000, value=1000, step=100)
start_date = st.sidebar.date_input('Start Date', value=datetime.now() - timedelta(days=365))
end_date = st.sidebar.date_input('End Date', value=datetime.now())
volatility_adjustment = st.sidebar.slider('Volatility Adjustment Factor:', min_value=0.5, max_value=2.0, value=1.0, step=0.1)
investment_amount = st.sidebar.number_input('Investment Amount ($):', min_value=100, max_value=100000, value=1000)

# Introduction and description of the app
st.markdown("""
## What is Monte Carlo Simulation?
At its core, Monte Carlo Simulation is a computational technique that employs randomness to solve problems that might be deterministic in principle. It's particularly valuable for assessing the impact of risk and uncertainty in forecasting models, making it an indispensable tool for asset pricing, risk management, and portfolio optimization. By leveraging historical stock price data, Monte Carlo simulations allow us to explore a wide range of future price scenarios.
## Exploring the App
This application invites you to conduct your own Monte Carlo simulations with ease. By inputting the ticker symbols of two stocks of your choice, you can compare their projected future price paths, visualizing not just the potential outcomes but also assessing the relative risk and volatility between them.

Enhanced with New Features
To cater to your specific analysis needs, here is a suite of customizable options:

1. **Forecast Length:** Adjust the slider to set the desired timeframe for your forecast, tailoring the simulation to your investment horizon.
1. **Simulation Runs:** Control the number of simulation runs to balance between computational intensity and the granularity of the results.
1. **Date Range for Historical Data:** Select the start and end dates to specify the historical data period you wish to consider for the simulation.
1. **Volatility Adjustment:** Experiment with different levels of volatility to understand its impact on stock price paths.
1. **Investment Amount:** Input your intended investment amount to see the expected return on investment, providing a tangible sense of potential gains or losses.
            
### How to Use This App
1. Select Your Stocks: Enter the ticker symbols for two stocks you want to analyze in the provided input fields.
1. Customize Your Simulation: Utilize the sidebar options to tailor the simulation parameters to your preferences.
1. Analyze the Results: Examine the visualized simulations and comparative analyses to inform your investment decisions.

Let's get started!
""")

# Creating two columns for ticker symbol inputs
col1, col2 = st.columns(2)

with col1:
    # Input for the first ticker symbol
    ticker1 = st.text_input('Enter First Ticker Symbol:', placeholder='e.g., AAPL')

with col2:
    # Input for the second ticker symbol
    ticker2 = st.text_input('Enter Second Ticker Symbol:', placeholder='e.g., MSFT')


# Adjusted Function to Download Stock Data for Custom Date Range
def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data['Adj Close']

# Function for Monte Carlo simulation
# Adjust the simulation to include 'volatility_adjustment'
def monte_carlo_simulation(start_price, days, dt, mu, sigma, runs, volatility_adjustment):
    sigma_adjusted = sigma * volatility_adjustment
    result = np.zeros((days + 1, runs))
    result[0] = start_price  # Initialize the first day to the start_price for all runs
    for t in range(1, days + 1):
        shock = np.random.normal(mu * dt, sigma_adjusted * np.sqrt(dt), runs)
        result[t] = result[t - 1] + result[t - 1] * shock
    return result

# Function to run simulation and plot for a given ticker
def run_simulation_for_ticker(ticker, forecast_length, num_runs, start_date, end_date, volatility_adjustment):
    # Download data for the custom date range
    data = download_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    start_price = data[-1]  # Use the last available price
    
    # Parameters for the simulation, adjusted for user input
    days = forecast_length
    dt = 1/days
    mu = data.pct_change().mean()  # Mean of daily returns
    sigma = data.pct_change().std()  # Standard deviation of daily returns
    
    # Pass 'num_runs' and 'volatility_adjustment' to the simulation
    simulation = monte_carlo_simulation(start_price, days, dt, mu, sigma, num_runs, volatility_adjustment)
    
    # Plotting the simulation paths with Plotly
    fig = go.Figure()
    for i in range(simulation.shape[1]):
        fig.add_trace(go.Scatter(x=np.arange(days + 1), y=simulation[:, i], mode='lines', opacity=0.5, line=dict(width=0.5), showlegend=False))
    fig.update_layout(title=f'Monte Carlo Simulation Paths for {ticker}',
                      xaxis_title='Days',
                      yaxis_title='Price',
                      yaxis=dict(fixedrange=False))
    st.plotly_chart(fig, use_container_width=True)
    
    return data, simulation

# Function to plot a comparison histogram of the final prices from simulations
def plot_comparison_histogram(simulation1, simulation2, ticker1, ticker2):
    final_prices1 = simulation1[-1, :]
    final_prices2 = simulation2[-1, :]
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=final_prices1, name=ticker1, opacity=0.75))
    fig.add_trace(go.Histogram(x=final_prices2, name=ticker2, opacity=0.75))
    fig.update_layout(title='Comparison of Final Price Distributions',
                      xaxis_title='Final Price',
                      yaxis_title='Frequency',
                      barmode='overlay')
    st.plotly_chart(fig, use_container_width=True)

def calculate_expected_roi(data, simulation, investment_amount):
    initial_price = data.iloc[0]  # Assuming the first price in the downloaded data is the initial price
    average_final_price = np.mean(simulation[-1, :])
    roi = (average_final_price - initial_price) / initial_price * investment_amount
    return roi

# Perform simulations and plot results if both tickers are provided
if ticker1 and ticker2:
    # Display headers before running simulations to clearly separate sections
    st.markdown(f"### Running Monte Carlo Simulations for {ticker1} and {ticker2}")
    
    # Run simulations automatically when sidebar inputs change
    st.markdown(f"#### Monte Carlo Simulation for {ticker1}")
    data1, simulation1 = run_simulation_for_ticker(ticker1, forecast_length, num_runs, start_date, end_date, volatility_adjustment)
    
    st.markdown(f"#### Monte Carlo Simulation for {ticker2}")
    data2, simulation2 = run_simulation_for_ticker(ticker2, forecast_length, num_runs, start_date, end_date, volatility_adjustment)

    # Comparative analysis
    st.markdown("### Comparative Analysis of Final Price Distributions")
    plot_comparison_histogram(simulation1, simulation2, ticker1, ticker2)

    # Ensure ROI calculations are performed after simulations
    expected_roi_ticker1 = calculate_expected_roi(data1, simulation1, investment_amount)
    expected_roi_ticker2 = calculate_expected_roi(data2, simulation2, investment_amount)

    roi_percentage_ticker1 = (expected_roi_ticker1 / investment_amount) * 100
    roi_percentage_ticker2 = (expected_roi_ticker2 / investment_amount) * 100

    st.markdown("## Expected Return on Investment")
    st.markdown(f"Given an investment of **${investment_amount:,.2f}** in each company, based on the parameters and the length of the window forecasted:")
    st.markdown(f"- For **{ticker1}**: Expected ROI is **${expected_roi_ticker1:,.2f}** ({roi_percentage_ticker1:.2f}%)")
    st.markdown(f"- For **{ticker2}**: Expected ROI is **${expected_roi_ticker2:,.2f}** ({roi_percentage_ticker2:.2f}%)")


# Embedding a YouTube video with an introduction
st.markdown("""
## Check Out this Video on Monte Carlo Simulations
This is a great video that offers insights into the Monte Carlo method, including its mathematical foundations and practical applications in finance. 
Understanding these principles are critical going forward! 
""")

# Use columns to center the video in the middle column
left_spacer, video_column, right_spacer = st.columns([1, 10, 1])  # Adjust the ratios as needed

with video_column:
    # Display the video in the middle column
    st.video('https://youtu.be/7ESK5SaP-bc?si=kqXG0_G9_ANA-kMU')
