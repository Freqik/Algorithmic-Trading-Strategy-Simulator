import React, { useState } from 'react';
import BacktestConfig from './components/BacktestConfig';
import EquityChart from './components/EquityChart';
import PriceChart from './components/PriceChart';
import KPIGrid from './components/KPIGrid';
import { runBacktest } from './services/api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleRunBacktest = async (payload) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await runBacktest(payload);
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Helper to prepare chart data by merging equity curve and trade markers.
   */
  const prepareChartData = () => {
    if (!results) return [];

    // Merge Benchmark + Equity
    // We assume index alignment or map via date. 
    // Backend returns lists. We need to zip them or Map by date.
    // For strictness, let's build a map.

    const dataMap = new Map();

    // 1. Add Strategy Equity
    results.equity_curve.forEach(pt => {
      dataMap.set(pt.date, {
        date: pt.date,
        equity: pt.equity,
        price: 0 // Placeholder
      });
    });

    // 2. Add Benchmark
    if (results.benchmark && results.benchmark.equity_curve) {
      results.benchmark.equity_curve.forEach(pt => {
        if (dataMap.has(pt.date)) {
          const existing = dataMap.get(pt.date);
          existing.benchmark = pt.equity;

          // We use benchmark equity normalized as proxy for price visualization if needed, 
          // OR we can just plot price? 
          // Wait, our backend doesn't return raw price history directly in a separate list.
          // But! Benchmark Equity (if constant Shares=1 assumption) IS proportional to Price.
          // Benchmark: Buy at Day 1. Shares = Initial / Price_0.
          // Equity_t = Shares * Price_t.
          // Price_t = Equity_t / Shares.
          // So we can reconstruct price perfectly.
          const initialCap = results.benchmark.equity_curve[0].equity;
          // We don't have start price easily here unless we pass it. 
          // But we can just plot Benchmark Equity as a proxy for "Buy & Hold" performance.
          // For the Price Chart, user wanted Price. 
          // Let's rely on Benchmark Equity as the "Buy & Hold" line which is enough context.

          // Reconstructing Price for markers:
          // Normalized Price = Equity
          existing.price = pt.equity;
        }
      });
    }

    // 3. Add Trade Markers
    // We match trade dates to chart dates.
    if (results.trades) {
      results.trades.forEach(trade => {
        // Entry
        if (dataMap.has(trade.entry_date)) {
          dataMap.get(trade.entry_date).buy_marker = dataMap.get(trade.entry_date).price; // Plot at price/equity level
          dataMap.get(trade.entry_date).action = 'BUY';
        }
        // Exit
        if (dataMap.has(trade.exit_date)) {
          dataMap.get(trade.exit_date).sell_marker = dataMap.get(trade.exit_date).price;
          dataMap.get(trade.exit_date).action = 'SELL';
        }
      });
    }

    return Array.from(dataMap.values()).sort((a, b) => new Date(a.date) - new Date(b.date));
  };

  const chartData = prepareChartData();

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">

        {/* Header */}
        <header>
          <h1 className="text-3xl font-bold text-gray-900">Algo Trading Simulator</h1>
          <p className="text-gray-500 mt-1">Professional Grade Backtesting Engine</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Configuration */}
          <div className="lg:col-span-1">
            <BacktestConfig onRunBacktest={handleRunBacktest} isLoading={isLoading} />

            {/* Error State */}
            {error && (
              <div className="mt-4 bg-red-50 border-l-4 border-red-500 p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-red-700 font-medium">Error Execution Failed</p>
                    <p className="text-sm text-red-600">{error}</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Right Column: Visualization */}
          <div className="lg:col-span-2 space-y-6">
            {!results && !isLoading && !error && (
              <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg h-96 flex flex-col items-center justify-center text-gray-400 p-8 text-center">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <h3 className="mt-2 text-sm font-medium text-gray-900">No Backtest Results</h3>
                <p className="mt-1 text-sm text-gray-500">Select a strategy and click 'Run Backtest' to see performance metrics and charts.</p>
              </div>
            )}

            {results && (
              <>
                <KPIGrid metrics={results.metrics} />
                <EquityChart data={chartData} />
                <PriceChart data={chartData} />
              </>
            )}

            {isLoading && (
              <div className="h-96 flex items-center justify-center space-x-2">
                <div className="w-4 h-4 bg-blue-600 rounded-full animate-bounce"></div>
                <div className="w-4 h-4 bg-blue-600 rounded-full animate-bounce delay-75"></div>
                <div className="w-4 h-4 bg-blue-600 rounded-full animate-bounce delay-150"></div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
