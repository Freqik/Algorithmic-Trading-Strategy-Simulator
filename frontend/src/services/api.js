import axios from 'axios';

// Create Axios Instance with Base URL
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Runs a backtest simulation.
 * 
 * @param {Object} payload - The backtest request payload
 * @param {string} payload.ticker - Stock symbol
 * @param {string} payload.start_date - YYYY-MM-DD
 * @param {string} payload.end_date - YYYY-MM-DD
 * @param {string} payload.strategy - Strategy name
 * @param {number} payload.initial_capital - Starting cash
 * @param {Object} payload.parameters - Strategy parameters
 * 
 * @returns {Promise<Object>} Backend response data (metrics, equity curve, etc.)
 * @throws {Error} User-friendly error message
 */
export const runBacktest = async (payload) => {
    try {
        const response = await api.post('/backtest', payload);
        return response.data;
    } catch (error) {
        // Detailed Error Handling
        if (error.response) {
            // Server responded with a status outside 2xx
            const message = error.response.data?.detail || 'An error occurred on the server.';
            throw new Error(message);
        } else if (error.request) {
            // No response received (Network Error)
            throw new Error('Network error: Unable to connect to the backend server.');
        } else {
            // Request setup error
            throw new Error(error.message || 'Unexpected error occurred.');
        }
    }
};

export default api;
