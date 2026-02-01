from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Dict, Any, Optional

class BacktestRequest(BaseModel):
    ticker: str = Field(..., min_length=1, description="Stock ticker symbol (e.g., AAPL)")
    start_date: date = Field(..., description="Start date of the backtest")
    end_date: date = Field(..., description="End date of the backtest")
    initial_capital: float = Field(100000.0, gt=0, description="Initial capital in USD")
    strategy: str = Field(..., description="Strategy name (e.g., ma_crossover)")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Strategy parameters")
    
    @field_validator('ticker')
    def uppercase_ticker(cls, v):
        return v.upper()

    @field_validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values.data and v <= values.data['start_date']:
            raise ValueError('end_date must be after start_date')
        return v
