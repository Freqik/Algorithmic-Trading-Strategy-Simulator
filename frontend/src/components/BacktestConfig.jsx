import React, { useState } from 'react';
import StrategySelector from './StrategySelector';
import ParameterForm from './ParameterForm';
import RunBacktest from './RunBacktest';
import { getStrategyDefaults } from '../utils/strategies';

const BacktestConfig = ({ onRunBacktest, isLoading }) => {
    const [ticker, setTicker] = useState('AAPL');
    const [startDate, setStartDate] = useState('2020-01-01');
    const [endDate, setEndDate] = useState('2023-01-01');
    const [initialCapital, setInitialCapital] = useState(100000);
    const [strategy, setStrategy] = useState('ma_crossover');
    const [parameters, setParameters] = useState(getStrategyDefaults('ma_crossover'));
    const [error, setError] = useState(null);

    const handleStrategyChange = (newStrategy) => {
        setStrategy(newStrategy);
        setParameters(getStrategyDefaults(newStrategy));
    };

    const handleParamChange = (name, value) => {
        setParameters(prev => ({
            ...prev,
            [name]: parseFloat(value) || 0
        }));
    };

    const handleSubmit = () => {
        setError(null);
        if (!ticker || !startDate || !endDate) {
            setError("Please fill in all required fields.");
            return;
        }

        const payload = {
            ticker: ticker.toUpperCase(),
            start_date: startDate,
            end_date: endDate,
            initial_capital: parseFloat(initialCapital),
            strategy,
            parameters
        };

        onRunBacktest(payload);
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 space-y-6">
            <h2 className="text-xl font-semibold text-gray-800">Backtest Configuration</h2>

            {/* Asset & Dates */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Ticker Symbol</label>
                    <input
                        type="text"
                        value={ticker}
                        onChange={(e) => setTicker(e.target.value.toUpperCase())}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                        placeholder="e.g. AAPL"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Initial Capital</label>
                    <input
                        type="number"
                        value={initialCapital}
                        onChange={(e) => setInitialCapital(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Start Date</label>
                    <input
                        type="date"
                        value={startDate}
                        onChange={(e) => setStartDate(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">End Date</label>
                    <input
                        type="date"
                        value={endDate}
                        onChange={(e) => setEndDate(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                    />
                </div>
            </div>

            <hr className="border-gray-200" />

            {/* Strategy Selection */}
            <StrategySelector
                selectedStrategy={strategy}
                onChange={handleStrategyChange}
            />

            {/* Dynamic Parameters */}
            <ParameterForm
                strategy={strategy}
                parameters={parameters}
                onChange={handleParamChange}
            />

            {/* Error Message */}
            {error && (
                <div className="text-red-600 text-sm bg-red-50 p-2 rounded">
                    {error}
                </div>
            )}

            {/* Run Button */}
            <RunBacktest
                onClick={handleSubmit}
                isLoading={isLoading}
                disabled={!ticker || !startDate || !endDate}
            />
        </div>
    );
};

export default BacktestConfig;
