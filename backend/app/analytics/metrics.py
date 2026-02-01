import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

# Annualization factor for daily data
TRADING_DAYS = 252

def calculate_metrics(equity_curve: List[Dict[str, Any]], trades: List[Dict[str, Any]], initial_capital: float) -> Dict[str, float]:
    """
    Calculates Performance Metrics based on equity curve and trade list.
    Robustly handles edge cases like empty data, insufficient periods, or no trades.
    
    Returns default zeroed metrics on failure rather than crashing.
    """
    
    # Defaults
    metrics = {
        "total_return": 0.0,
        "cagr": 0.0,
        "sharpe_ratio": 0.0,
        "volatility": 0.0,
        "max_drawdown": 0.0,
        "win_rate": 0.0,
        "profit_factor": 0.0,
        "avg_trade_net_pnl": 0.0,
        "total_trades": len(trades) if trades else 0
    }

    # Guard: Empty Equity Curve
    if not equity_curve:
        logger.warning("calculate_metrics called with empty equity_curve.")
        return metrics

    try:
        # Convert equity curve to DataFrame
        df = pd.DataFrame(equity_curve)
        
        # Guard: Incomplete Data Structure
        if 'equity' not in df.columns or 'date' not in df.columns:
            logger.error("equity_curve missing required columns 'equity' or 'date'.")
            return metrics

        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        # Guard: Insufficient Data Points for Statistics
        if len(df) < 2:
            logger.warning("Insufficient data points (< 2) for metric calculation.")
            return metrics

        # Daily Returns
        # pct_change() puts NaN in first row, so we drop it
        df['returns'] = df['equity'].pct_change().dropna()
        
        # 1. Total Return
        final_equity = df['equity'].iloc[-1]
        metrics["total_return"] = (final_equity - initial_capital) / initial_capital
        
        # 2. Volatility (Annualized)
        if len(df['returns']) > 1:
            metrics["volatility"] = df['returns'].std() * np.sqrt(TRADING_DAYS)

        # 3. Sharpe Ratio
        if metrics["volatility"] > 1e-9: # Avoid division by zero
            # Assuming 0% risk-free rate
            mean_ret = df['returns'].mean() * TRADING_DAYS
            metrics["sharpe_ratio"] = mean_ret / metrics["volatility"]
            
        # 4. Max Drawdown
        df['peak'] = df['equity'].cummax()
        # Avoid division by zero if peak is 0 (unlikely for equity but possible)
        df['drawdown'] = 0.0
        mask = df['peak'] > 0
        df.loc[mask, 'drawdown'] = (df.loc[mask, 'equity'] - df.loc[mask, 'peak']) / df.loc[mask, 'peak']
        metrics["max_drawdown"] = df['drawdown'].min()
        
        # 5. CAGR
        start_date = df.index[0]
        end_date = df.index[-1]
        days = (end_date - start_date).days
        
        if days > 0:
            years = days / 365.25
            # Ensure base is positive for exponentiation
            if final_equity > 0 and initial_capital > 0:
                 metrics["cagr"] = (final_equity / initial_capital) ** (1 / years) - 1
        
    except Exception as e:
        logger.error(f"Error calculating equity metrics: {e}")
        # Return whatever we calculated so far, or defaults
        return metrics

    # 6. Trade Metrics
    if trades:
        try:
            pnls = [t.get('pnl_net', 0.0) for t in trades]
            winning_trades = [p for p in pnls if p > 0]
            losing_trades = [p for p in pnls if p <= 0]
            
            total_trades = len(pnls)
            
            if total_trades > 0:
                metrics["win_rate"] = len(winning_trades) / total_trades
            
            metrics["avg_trade_net_pnl"] = np.mean(pnls) if pnls else 0.0
            
            gross_profit = sum(winning_trades)
            gross_loss = abs(sum(losing_trades))
            
            if gross_loss > 1e-9:
                metrics["profit_factor"] = gross_profit / gross_loss
            else:
                metrics["profit_factor"] = float('inf') if gross_profit > 0 else 0.0
                
        except Exception as e:
             logger.error(f"Error calculating trade metrics: {e}")

    return metrics
