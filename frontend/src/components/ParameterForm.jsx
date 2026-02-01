import React from 'react';
import { STRATEGIES } from '../utils/strategies';

const ParameterForm = ({ strategy, parameters, onChange }) => {
    const stratDefinition = STRATEGIES.find(s => s.id === strategy);

    if (!stratDefinition || stratDefinition.params.length === 0) {
        return null;
    }

    return (
        <div className="space-y-4">
            <h3 className="text-sm font-medium text-gray-900">Strategy Parameters</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {stratDefinition.params.map((param) => (
                    <div key={param.name}>
                        <label className="block text-xs font-medium text-gray-500 mb-1">
                            {param.label}
                        </label>
                        <input
                            type={param.type}
                            value={parameters[param.name] ?? ''}
                            onChange={(e) => onChange(param.name, e.target.value)}
                            min={param.min}
                            max={param.max}
                            step={param.step || 1}
                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
                        />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ParameterForm;
