import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings configuration.
    Loads values from environment variables or .env file.
    """
    APP_NAME: str = "AlgoTradingSimulator"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    
    # Data Data
    DATA_PROVIDER: str = "yfinance"
    
    # Backtest Defaults
    DEFAULT_INITIAL_CAPITAL: float = 100000.0
    DEFAULT_START_DATE: str = "2010-01-01"
    DEFAULT_END_DATE: str = "2023-12-31"
    
    # Trading Costs
    TRANSACTION_COST: float = 0.001
    SLIPPAGE: float = 0.0005
    
    # CORS
    FRONTEND_URL: str = "http://localhost:5173"
    
    @property
    def cors_origins(self) -> List[str]:
        return ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
