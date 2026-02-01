import React from 'react';

const MetricCard = ({ label, value, tooltip, format = 'number' }) => {
    let formattedValue = value;
    let colorClass = 'text-gray-900';

    if (value === undefined || value === null) {
        formattedValue = '-';
    } else {
        if (format === 'percent') {
            formattedValue = `${(value * 100).toFixed(2)}%`;
            if (value > 0) colorClass = 'text-green-600';
            if (value < 0) colorClass = 'text-red-600';
        } else if (format === 'currency') {
            formattedValue = `$${value.toFixed(2)}`;
        } else if (format === 'decimal') {
            formattedValue = value.toFixed(2);
        }
    }

    return (
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 relative group hover:shadow-md transition-shadow">
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wider">{label}</p>
            <p className={`mt-1 text-2xl font-semibold ${colorClass}`}>
                {formattedValue}
            </p>

            {/* Tooltip */}
            <div className="absolute opacity-0 group-hover:opacity-100 transition-opacity bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-48 bg-gray-900 text-white text-xs rounded p-2 z-10 pointer-events-none">
                {tooltip}
                <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-900"></div>
            </div>
        </div>
    );
};

export default MetricCard;
