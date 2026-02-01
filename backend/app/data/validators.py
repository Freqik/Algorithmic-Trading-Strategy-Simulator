import pandas as pd
from typing import List, Optional

REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]

class DataValidationError(Exception):
    """Custom exception for data validation failures."""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message)
        self.details = details

def validate_market_data(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Validates the structure and integrity of market data.
    
    Args:
        df: The pandas DataFrame containing historical data.
        ticker: The symbol being validated (for error messages).
        
    Returns:
        The validated DataFrame (potentially with types cast).
        
    Raises:
        DataValidationError: If validation fails.
    """
    # 1. Check if empty
    if df is None or df.empty:
        raise DataValidationError(f"No data found for ticker: {ticker}")

    # 2. Check Required Columns
    # yfinance sometimes returns MultiIndex columns or extra columns. 
    # We expect a flat index with standard OHLCV.
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise DataValidationError(
            f"Missing required columns for {ticker}: {missing_cols}",
            details={"missing": missing_cols, "found": list(df.columns)}
        )

    # 3. Check for NaNs in critical columns
    # We allow some NaNs in Volume if necessary, but Price data must be solid.
    null_counts = df[REQUIRED_COLUMNS].isnull().sum()
    if null_counts.sum() > 0:
        # For simulation, we can't accept gaps in price data easily.
        # Dropping small % of rows might be okay, but for now we strictly reject or warn.
        # Let's strictly reject if any price data is missing.
        price_nulls = null_counts.drop("Volume", errors='ignore').sum()
        if price_nulls > 0:
             raise DataValidationError(
                f"Data for {ticker} contains {price_nulls} missing price values.",
                details=null_counts.to_dict()
            )

    # 4. Check Index Monotonicity (Time Sorted)
    if not df.index.is_monotonic_increasing:
        df = df.sort_index()
    
    # 5. Check for Duplicates
    if df.index.has_duplicates:
        df = df[~df.index.duplicated(keep='first')]

    return df
