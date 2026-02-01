# Algorithmic Trading Strategy Simulator

## 1. Project Title & Overview

**Algorithmic Trading Strategy Simulator** is a robust, full-stack web application designed to backtest and analyze quantitative trading strategies against historical market data.

It serves as a dedicated platform for **strategy evaluation**, allowing users to simulate the performance of logic-based trading rules (such as Moving Average Crossovers, RSI Mean Reversion, and Momentum) without financial risk. The system provides a comprehensive suite of risk-adjusted metrics, interactive equity curves, and trade-by-trade analysis to determine the viability of a given strategy.

**Note:** This is a **backtesting and analysis tool**, not a live trading execution bot. It is designed for research, education, and strategy validation.

## 2. Why This Project Exists

In the domain of quantitative finance, the ability to predict future prices is often secondary to the ability to manage risk and execute varying strategies consistently. A common pitfall for emerging quants is the reliance on intuition rather than empirical evidence.

This project was built to solve the **validation gap**: the lack of accessible, transparent tools to rigorously test trading hypotheses before capital deployment. By simulating strategies over extended historical periods, this tool allows users to:
*   Identify regime-dependent performance (e.g., how a strategy performs in bull vs. bear markets).
*   Quantify downside risk through metrics like Max Drawdown and Volatility.
*   Understand the mechanics of trade lifecycle and costs (slippage/commissions).

## 3. High-Level System Architecture

The application follows a clean **Client-Server Architecture** with a strict separation of concerns, ensuring scalability and maintainability.

*   **Frontend (Visualization Layer):** A React-based Single Page Application (SPA) that handles user configuration, interactive charting (Recharts), and KPI display. It communicates with the backend via a RESTful API.
*   **Backend (Engine Layer):** A FastAPI server that orchestrates the simulation.
    *   **Data Ingestion:** Fetches historical OHLCV data from external providers (Yahoo Finance) or falls back to synthetic geometric brownian motion models when rate-limited.
    *   **Engine Core:** Wraps the **Backtrader** framework to execute event-driven simulations.
    *   **Strategy Registry:** A modular system to dynamically load and instantiate trading logic.
    *   **Analytics Module:** Post-simulation processing to calculate risk metrics (Sharpe, Sortino, CAGR) and generate benchmarks.

## 4. Key Features

*   **Event-Driven Backtesting:** Simulates trading bar-by-bar to prevent lookahead bias and accurately model execution path.
*   **Realistic Execution assumptions:** Incorporates configurable Transaction Costs (Commissions) and Slippage to model real-world friction.
*   **Risk-Adjusted Performance Metrics:** Goes beyond simple "Total Return" to calculate Sharpe Ratio, Volatility, Max Drawdown, Win Rate, and Profit Factor.
*   **Benchmark Comparison:** Automatically compares strategy performance against a standard "Buy & Hold" benchmark for the same asset and period.
*   **Modular Strategy System:** Easily extensible architecture supporting multiple strategy types (Trend Following, Mean Reversion, Momentum).
*   **Interactive Visualization:** Dynamic Equity Curves and Price Charts with overlaid trade entry/exit points.

## 5. Tech Stack

**Backend**
*   **Language:** Python 3.12+
*   **Framework:** FastAPI (High-performance Async I/O)
*   **Core Engine:** Backtrader (Event-driven backtesting)
*   **Data Analysis:** Pandas, NumPy
*   **Data Source:** yfinance (Yahoo Finance API)

**Frontend**
*   **Framework:** React 18 (Vite)
*   **Styling:** Tailwind CSS (Utility-first design)
*   **Visualization:** Recharts (Composable charting library)
*   **State/Network:** Axios

## 6. How to Run Locally

### Prerequisites
*   Python 3.10+
*   Node.js 16+
*   Git

### 1. Backend Setup
Navigate to the root directory and set up the Python environment.

```bash
# Navigate to the backend folder (or root if using absolute imports)
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the API Server
# Note: Run this from the project root if using absolute package imports
uvicorn backend.app.main:app --reload
```
The Backend will start at `http://localhost:8000`.

### 2. Frontend Setup
Open a new terminal and navigate to the frontend directory.

```bash
cd frontend

# Install dependencies
npm install

# Start the Development Server
npm run dev
```
The Frontend will start at `http://localhost:5173`.

### 3. Usage
Open `http://localhost:5173` in your browser. Select a Ticker (e.g., AAPL), choose a Strategy, and click **Run Backtest**.

## 7. Verification & Stability

This system has undergone rigorous verification to ensure stability under various edge cases. It adheres to a philosophy of **graceful degradation**:

*   **Insufficient Data:** If a user selects a timeframe too short for the strategy to initialize (e.g., a 200-day MA on 1 month of data), the system detects this and returns a neutral "0 trades" result rather than crashing.
*   **Parameter Validation:** All inputs are strictly validated against the strategy's requirements. Mismatched parameters are caught early with descriptive errors.
*   **API Resilience:** The system includes automatic sanitization of outputs (handling `NaN` or `Infinity` values) to ensure the Frontend never receives malformed JSON.

## 8. Limitations & Assumptions

*   **No Live Trading:** This system cannot execute orders on a real exchange.
*   **Daily Granularity:** The simulation operates on Daily (1D) candles. Intraday price movements are not modeled.
*   **Survivorship Bias:** Ticker selection is manual; delisted companies are not automatically accounted for.
*   *For a detailed list of constraints, please refer to the `LIMITATIONS.md` file.*

## 9. Project Status

✅ **Status: Stable / Completed**

The core architecture, strategy engine, and visualization layers are fully implemented and verified. The system supports extension for additional strategies and more complex risk models.
