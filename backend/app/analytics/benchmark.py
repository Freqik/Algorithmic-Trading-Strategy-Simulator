import pandas as pd
from typing import Dict, Any, List

def calculate_benchmark(data: pd.DataFrame, initial_capital: float) -> Dict[str, Any]:
    """
    Simulates a Buy & Hold Benchmark.
    Buys at first Close, Holds until last Close.
    No transaction costs or slippage for the benchmark.
    
    Args:
        data: DataFrame with at least 'Close' column.
        initial_capital: Starting cash.
        
    Returns:
        Dict containing benchmark equity curve and metrics.
    """
    if data.empty:
        return {}

    # Calculate Buy & Hold Equity Curve
    # Equity = (Current_Price / Entry_Price) * Initial_Capital
    entry_price = data['Close'].iloc[0]
    
    # Vectorized calculation
    equity_series = (data['Close'] / entry_price) * initial_capital
    
    # Create Equity Curve List
    equity_curve = []
    for date, value in equity_series.items():
        equity_curve.append({
            "date": date,
            "equity": value,
            "cash": 0.0 # Fully invested
        })
        
    # Calculate basic return for benchmark (we can reuse the main metrics function if we fake trades)
    # But for benchmark we mostly care about the curve and total return.
    
    final_val = equity_series.iloc[-1]
    total_return = (final_val - initial_capital) / initial_capital
    
    return {
        "equity_curve": equity_curve,
        "metrics": {
            "total_return": float(total_return),
            "final_value": float(final_val)
        }
    }
