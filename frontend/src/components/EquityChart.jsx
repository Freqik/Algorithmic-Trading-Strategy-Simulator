import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

/**
 * Renders the Equity Curve comparison chart.
 * 
 * @param {Object} props
 * @param {Array} props.data - Merged data array [{ date, equity, benchmark }]
 */
const EquityChart = ({ data }) => {
    if (!data || data.length === 0) {
        return <div className="h-64 flex items-center justify-center text-gray-400">No data available</div>;
    }

    const formatYAxis = (tick) => {
        if (tick >= 1000) return `${(tick / 1000).toFixed(0)}k`;
        return tick;
    };

    return (
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-lg font-medium text-gray-800 mb-4">Equity Curve</h3>
            <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} />
                        <XAxis
                            dataKey="date"
                            tickFormatter={(str) => new Date(str).toLocaleDateString()}
                            minTickGap={30}
                            style={{ fontSize: '12px' }}
                        />
                        <YAxis
                            domain={['auto', 'auto']}
                            tickFormatter={formatYAxis}
                            style={{ fontSize: '12px' }}
                        />
                        <Tooltip
                            formatter={(value) => [`$${value.toFixed(2)}`, 'Equity']}
                            labelFormatter={(label) => new Date(label).toLocaleDateString()}
                        />
                        <Legend />
                        <Line
                            type="monotone"
                            dataKey="equity"
                            name="Strategy"
                            stroke="#2563eb"
                            strokeWidth={2}
                            dot={false}
                        />
                        <Line
                            type="monotone"
                            dataKey="benchmark"
                            name="Benchmark"
                            stroke="#9ca3af"
                            strokeWidth={2}
                            strokeDasharray="5 5"
                            dot={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default EquityChart;
