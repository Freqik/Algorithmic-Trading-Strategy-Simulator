# Known Limitations & Assumptions

This document outlines the scope capabilities and inherent limitations of the Algorithmic Trading Strategy Simulator.

## 1. Simulation Nature (No Live Trading)
-   **Strictly Offline**: This system is a historical simulator (backtester). It **cannot** execute trades on real exchanges.
-   **No Broker Integration**: There are no APIs connected to brokerage accounts (e.g., IBKR, Alpaca).

## 2. Market Data & Execution Assumptions
-   **Daily Candles**: The simulation operates on daily OHLCV data. Intra-day price movements are not simulated.
-   **Execution Price**: Trades are assumed to execute at the **Close** price of the signal bar (or Next Open, depending on specific strategy logic configured in Backtrader).
-   **No Corporate Actions**: The current data provider integration does not automatically adjust for stock splits or dividends effectively in all scenarios. Re-investment of dividends is not modeled.
-   **Survivorship Bias**: Historical data fetches usually list currently active tickers. Delisted companies are not included, potentially skewing long-term aggregate performance results upwards.

## 3. Financial Calculations
-   **Approximations**: While transaction costs and slippage are modeled (e.g., 0.1% per trade), they are fixed estimates. Real market spread and impact vary dynamically.
-   **Risk-Free Rate**: Sharpe Ratio calculations assume a simplistic risk-free rate (often 0% or fixed) for "Excess Return" calculation unless otherwise specified.

## 4. Visualization
-   **Price Reconstruction**: The "Price Chart" visualizes the asset price. In some views, this may be reconstructed from the Benchmark Equity curve (which is linearly proportional to price in a Buy & Hold scenario). This is a visual proxy and may slightly deviate from raw adjusted close data due to mathematical rounding.

## 5. Disclaimer
-   **Not Financial Advice**: The results produced by this simulator are for **educational and engineering evaluation purposes only**. Past performance is not indicative of future results.
