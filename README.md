# Stock Price Forecasting with Monte Carlo Simulations

## Overview
This application leverages the power of Monte Carlo simulations to forecast future stock prices, providing users with insights into potential price paths, volatility, and risk associated with selected stocks. By inputting ticker symbols for two stocks, users can compare their future price trajectories based on historical data, enabling informed investment decisions.

## What is Monte Carlo Simulation?
Monte Carlo Simulation is a statistical technique that uses randomness to predict the outcome of a process that is deterministic in nature but has inherent uncertainty due to random variables. In the realm of finance, it is a critical tool for modeling the probability of various outcomes in markets, where the future price of assets is unpredictable. This method calculates multiple scenarios of future price movements based on historical data, offering a comprehensive view of potential risks and volatility.

## Features
- **Customizable Forecast Length**: Users can define the length of the forecast period, tailoring the analysis to short-term or long-term investment strategies.
- **Adjustable Number of Simulations**: The app allows for varying the number of simulation runs, offering flexibility in the depth of analysis.
- **Historical Data Range Selection**: Users can select the start and end dates for the historical data used in simulations, providing control over the data influencing the forecast.
- **Volatility Adjustment**: This feature enables users to adjust the volatility factor, exploring how changes in market volatility might affect stock prices.
- **Investment Amount Calculation**: Input an investment amount to calculate the expected return based on the simulation results, adding a practical dimension to the analysis.

## Monte Carlo Simulation Details

### Key Variables Explained
- **`dt` (Time Step)**: Represents one trading day, typically 1/252, reflecting the annual trading days. It's used to scale the mean and volatility for daily price simulation.

- **`mu` (Expected Return)**: The average daily return calculated from historical data, guiding the expected trend in stock price movement in our simulations.

- **`sigma` (Volatility)**: Measures the stock's price fluctuation level. Higher `sigma` means higher risk and uncertainty in price movement.

### Monte Carlo Simulation Function
This central function simulates future stock price paths using `dt`, `mu`, and `sigma`. It performs the following steps:

1. Generates random daily price variations reflecting the stock's historical volatility (`sigma`) and expected return (`mu`).
2. Applies these variations sequentially to simulate a price path for the defined forecast period.
3. Repeats the simulation for many runs to model a wide range of possible future price paths.

### Purpose and Application
These variables allow the simulation to balance historical stock trends with the inherent uncertainty in market movements, providing a realistic range of future stock prices. This method offers valuable insights into potential risk and price behavior, aiding in informed investment decision-making.


## How It Works
1. **Data Retrieval**: The app downloads historical stock price data for the selected tickers within the user-defined date range.
2. **Simulation Parameters**:
   - **Forecast Length**: Determines the number of days into the future for which the price paths are simulated.
   - **Number of Runs**: Specifies how many individual simulation paths will be calculated for each stock.
   - **Volatility Adjustment**: Alters the standard deviation of the stock's daily returns, affecting the spread of simulated price paths.
3. **Monte Carlo Simulation**: For each stock, the app simulates multiple price paths based on historical returns, adjusted for user-defined volatility. Each path represents a potential future trajectory of the stock price.
4. **ROI Calculation**: The app calculates the expected return on investment by comparing the average final price from the simulations to the initial investment, adjusted for the amount invested.

## Using the App
1. Enter the ticker symbols for two stocks in the designated input fields.
2. Adjust the simulation parameters via the sidebar to fit your analysis needs.
3. Analyze the visualized future price paths and the comparative histogram of final prices to gauge potential outcomes.
4. Review the expected ROI based on your investment amount and the simulations to inform your investment strategy.

## Conclusion
This Stock Price Forecasting app provides a dynamic and interactive platform for investors to assess potential future performances of stocks using Monte Carlo simulations. By offering customizable parameters and detailed visualizations, it empowers users to make data-driven investment decisions.
