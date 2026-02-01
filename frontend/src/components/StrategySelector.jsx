import React from 'react';
import { STRATEGIES } from '../utils/strategies';

const StrategySelector = ({ selectedStrategy, onChange }) => {
    return (
        <div>
            <label className="block text-sm font-medium text-gray-700">Strategy</label>
            <div className="mt-1">
                <select
                    value={selectedStrategy}
                    onChange={(e) => onChange(e.target.value)}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                >
                    {STRATEGIES.map(strat => (
                        <option key={strat.id} value={strat.id}>
                            {strat.name}
                        </option>
                    ))}
                </select>
                <p className="mt-1 text-xs text-gray-500">
                    {STRATEGIES.find(s => s.id === selectedStrategy)?.description}
                </p>
            </div>
        </div>
    );
};

export default StrategySelector;
