import React from 'react';
import { ComposedChart, Line, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

/**
 * Renders the Asset Price Chart with Buy/Sell markers.
 * Uses the Normalized Benchmark Equity as a proxy for Price movement.
 * 
 * @param {Object} props
 * @param {Array} props.data - array [{ date, price, buy_marker, sell_marker }]
 */
const PriceChart = ({ data }) => {
    if (!data || data.length === 0) {
        return <div className="h-64 flex items-center justify-center text-gray-400">No data available</div>;
    }

    const formatYAxis = (tick) => {
        return tick.toFixed(2);
    };

    // Custom shape for markers
    const renderShape = (props) => {
        const { cx, cy, payload } = props;
        if (payload.action === 'BUY') {
            return (
                <path d={`M${cx},${cy + 5} L${cx - 5},${cy + 15} L${cx + 5},${cy + 15} Z`} fill="#16a34a" />
            ); // Green Triangle Up
        }
        if (payload.action === 'SELL') {
            return (
                <path d={`M${cx},${cy - 5} L${cx - 5},${cy - 15} L${cx + 5},${cy - 15} Z`} fill="#dc2626" />
            ); // Red Triangle Down
        }
        return null;
    };

    return (
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-lg font-medium text-gray-800 mb-4">Price History & Trades</h3>
            <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <ComposedChart data={data}>
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
                            labelFormatter={(label) => new Date(label).toLocaleDateString()}
                        />
                        <Legend />
                        <Line
                            type="monotone"
                            dataKey="price"
                            name="Price (Reconstructed)"
                            stroke="#4b5563"
                            strokeWidth={1}
                            dot={false}
                        />
                        <Scatter
                            name="Buy"
                            dataKey="buy_marker"
                            shape={renderShape}
                            legendType="triangle"
                            fill="#16a34a"
                        />
                        <Scatter
                            name="Sell"
                            dataKey="sell_marker"
                            shape={renderShape}
                            legendType="triangle"
                            fill="#dc2626"
                        />
                    </ComposedChart>
                </ResponsiveContainer>
            </div>
            <div className="text-xs text-gray-500 mt-2 italic">
                * Price reconstructed from benchmark equity curve. Markers indicate trade entries/exits.
            </div>
        </div>
    );
};

export default PriceChart;
