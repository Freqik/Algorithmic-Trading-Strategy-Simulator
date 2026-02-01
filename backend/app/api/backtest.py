from fastapi import APIRouter, HTTPException
from backend.app.schemas.request import BacktestRequest
from backend.app.schemas.response import BacktestResponse
from backend.app.data.market_data import market_data_service, DataValidationError
from backend.app.engine.backtester import Backtester

# Strategy Imports
from backend.app.strategies.ma_crossover import MaCrossover
try:
    from backend.app.strategies.rsi_mean_reversion import RsiMeanReversion
except ImportError:
    RsiMeanReversion = None

try:
    from backend.app.strategies.momentum import MomentumStrategy
except ImportError:
    MomentumStrategy = None

from backend.app.analytics.metrics import calculate_metrics
from backend.app.analytics.benchmark import calculate_benchmark
from backend.app.core.config import settings
import logging
import traceback
import pandas as pd
import numpy as np
import math

router = APIRouter()
logger = logging.getLogger(__name__)

# Centralized Strategy Registry
STRATEGY_MAP = {
    "ma_crossover": MaCrossover,
    "rsi_mean_reversion": RsiMeanReversion,
    "momentum": MomentumStrategy
}

def sanitize_float(value: float) -> float:
    """Safely convert Infinity/NaN to 0.0 for JSON serialization."""
    if value is None:
        return 0.0
    if math.isinf(value) or math.isnan(value):
        return 0.0
    return float(value)

@router.post("/backtest", response_model=BacktestResponse)
async def run_backtest(request: BacktestRequest):
    """
    Execute a backtest for a given strategy and parameters.
    Wraps entire execution in try/except to prevent 500 crashes.
    """
    try:
        logger.info(f"Received backtest request for {request.ticker} with {request.strategy}")

        # 1. Validate Strategy
        strategy_cls = STRATEGY_MAP.get(request.strategy)
        if not strategy_cls:
            available = [k for k in STRATEGY_MAP.keys() if STRATEGY_MAP[k] is not None]
            raise HTTPException(
                status_code=400, 
                detail=f"Strategy '{request.strategy}' not found. Available: {available}"
            )

        # 2. Fetch Data
        data = market_data_service.fetch_historical_data(
            request.ticker, 
            str(request.start_date), 
            str(request.end_date)
        )
        
        # 2b. Normalize Columns (Verify consistency)
        data.columns = [c.capitalize() for c in data.columns]
        
        # 3. Run Backtest
        backtester = Backtester(
            strategy_cls=strategy_cls,
            data=data,
            params=request.parameters,
            initial_capital=request.initial_capital,
            transaction_cost=settings.TRANSACTION_COST,
            slippage=settings.SLIPPAGE
        )
        bt_result = backtester.run()
        
        # 4. Calculate Metrics
        metrics = calculate_metrics(
            bt_result['equity_curve'], 
            bt_result['trades'], 
            request.initial_capital
        )
        
        # 4b. Sanitize Metrics (Inf/NaN -> 0.0)
        sanitized_metrics = {k: sanitize_float(v) for k, v in metrics.items()}
        
        # 4c. Sanitize Trades (exit_price None -> 0.0)
        sanitized_trades = []
        for t in bt_result['trades']:
            t_clean = t.copy()
            t_clean['exit_price'] = sanitize_float(t.get('exit_price'))
            t_clean['entry_price'] = sanitize_float(t.get('entry_price'))
            t_clean['pnl'] = sanitize_float(t.get('pnl'))
            t_clean['pnl_net'] = sanitize_float(t.get('pnl_net'))
            t_clean['size'] = sanitize_float(t.get('size'))
            t_clean['duration'] = sanitize_float(t.get('duration'))
            sanitized_trades.append(t_clean)

        # 5. Calculate Benchmark
        try:
            benchmark_res = calculate_benchmark(data, request.initial_capital)
            # Sanitize benchmark metrics if they exist
            if benchmark_res and 'metrics' in benchmark_res:
                benchmark_res['metrics'] = {k: sanitize_float(v) for k, v in benchmark_res['metrics'].items()}
        except Exception as e:
            logger.error(f"Benchmark calculation failed: {e}")
            benchmark_res = None
        
        return {
            "metrics": sanitized_metrics,
            "equity_curve": bt_result['equity_curve'],
            "trades": sanitized_trades,
            "benchmark": benchmark_res
        }

    except HTTPException as e:
        raise e
    except DataValidationError as e:
        logger.error(f"Data error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.error(f"Execution error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        error_details = traceback.format_exc()
        logger.error(f"Unexpected error during backtest:\n{error_details}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}\nTraceback caught in handler."
        )
