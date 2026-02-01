export const STRATEGIES = [
    {
        id: 'ma_crossover',
        name: 'Moving Average Crossover',
        description: 'Buy when Short MA crosses above Long MA.',
        params: [
            { name: 'short_window', label: 'Short Window', type: 'number', default: 20, min: 1 },
            { name: 'long_window', label: 'Long Window', type: 'number', default: 50, min: 1 }
        ]
    },
    {
        id: 'rsi_mean_reversion',
        name: 'RSI Mean Reversion',
        description: 'Buy when RSI < Lower, Sell when RSI > Upper.',
        params: [
            { name: 'rsi_period', label: 'RSI Period', type: 'number', default: 14, min: 2 },
            { name: 'lower_threshold', label: 'Lower Threshold', type: 'number', default: 30, min: 0, max: 100 },
            { name: 'upper_threshold', label: 'Upper Threshold', type: 'number', default: 70, min: 0, max: 100 }
        ]
    },
    {
        id: 'momentum',
        name: 'Momentum Strategy',
        description: 'Trend following based on recent returns.',
        params: [
            { name: 'momentum_period', label: 'Momentum Period', type: 'number', default: 10, min: 1 },
            { name: 'threshold', label: 'Signal Threshold', type: 'number', default: 0.0, step: 0.001 }
        ]
    }
];

export const getStrategyDefaults = (strategyId) => {
    const strat = STRATEGIES.find(s => s.id === strategyId);
    if (!strat) return {};
    return strat.params.reduce((acc, param) => {
        acc[param.name] = param.default;
        return acc;
    }, {});
};
