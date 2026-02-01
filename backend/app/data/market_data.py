import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Optional
from backend.app.data.validators import validate_market_data, DataValidationError

logger = logging.getLogger(__name__)

class MarketDataService:
    def fetch_historical_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetches historical market data from yfinance.
        Falls back to mock data if yfinance is rate-limited or fails.
        """
        try:
            logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
            
            df = yf.download(
                ticker, 
                start=start_date, 
                end=end_date, 
                progress=False,
                auto_adjust=True
            )
            
            if df.empty:
                logger.warning(f"yfinance returned empty data for {ticker}. Attempting fallback...")
                return self.generate_mock_data(ticker, start_date, end_date)

            # yfinance with auto_adjust=True returns: Open, High, Low, Close, Volume
            # Ensure the index is Datetime
            df.index = pd.to_datetime(df.index)
            
            # Additional Handling for MultiIndex columns if necessary
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Validate
            df = validate_market_data(df, ticker)
            
            logger.info(f"Successfully fetched {len(df)} rows for {ticker}")
            return df

        except DataValidationError as e:
            logger.error(f"Validation error for {ticker}: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Failed to fetch data for {ticker}: {str(e)}")
            raise ValueError(f"Failed to fetch data for {ticker}: {str(e)}")

    def generate_mock_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Generates synthetic OHLCV data using a geometric brownian motion model.
        Used as a fallback when live data is unavailable.
        """
        logger.warning(f"Generating SCOPED MOCK DATA for {ticker}")
        
        dates = pd.date_range(start=start_date, end=end_date, freq='B')
        n = len(dates)
        
        if n == 0:
            # Fallback if dates are invalid, just give 30 days
            dates = pd.date_range(end=datetime.today(), periods=30, freq='B')
            n = len(dates)

        # Random Walk parameters
        start_price = 150.0
        mu = 0.0005  # Drift
        sigma = 0.02 # Volatility
        
        import numpy as np
        returns = np.random.normal(mu, sigma, n)
        price_path = start_price * (1 + returns).cumprod()
        
        # Create DataFrame
        df = pd.DataFrame(index=dates)
        df['close'] = price_path
        df['open'] = df['close'] * (1 + np.random.normal(0, 0.005, n))
        df['high'] = df[['open', 'close']].max(axis=1) * (1 + abs(np.random.normal(0, 0.01, n)))
        df['low'] = df[['open', 'close']].min(axis=1) * (1 - abs(np.random.normal(0, 0.01, n)))
        df['volume'] = np.random.randint(100000, 5000000, n)
        
        df.index.name = 'Date'
        
        # Ensure 'validate_market_data' passes
        df.sort_index(inplace=True)
        df.dropna(inplace=True)
        
        return df

# Singleton or utility usage
market_data_service = MarketDataService()
