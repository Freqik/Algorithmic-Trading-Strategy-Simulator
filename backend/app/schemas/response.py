from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date

class MetricCard(BaseModel):
    total_return: float
    cagr: float
    sharpe_ratio: float
    volatility: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    avg_trade_net_pnl: float
    total_trades: int

class EquityPoint(BaseModel):
    date: date
    equity: float
    cash: float

class TradeRecord(BaseModel):
    ticker: str
    entry_date: date
    exit_date: date
    entry_price: float
    exit_price: float
    pnl: float
    pnl_net: float
    size: float
    duration: float

class BenchmarkResult(BaseModel):
    equity_curve: List[EquityPoint]
    metrics: Dict[str, float]

class BacktestResponse(BaseModel):
    metrics: MetricCard
    equity_curve: List[EquityPoint]
    trades: List[TradeRecord]
    benchmark: Optional[BenchmarkResult] = None
