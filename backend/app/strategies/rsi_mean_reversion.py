import backtrader as bt
from backend.app.strategies.base import StrategyBase

class RsiMeanReversion(StrategyBase):
    """
    RSI Mean Reversion Strategy.
    - Buy when RSI < low_threshold (Oversold)
    - Sell when RSI > high_threshold (Overbought)
    
    Parameters:
    - period (14): RSI period
    - low_threshold (30): Buy signal
    - high_threshold (70): Sell signal
    """
    params = (
        ("rsi_period", 14),
        ("lower_threshold", 30),
        ("upper_threshold", 70),
    )

    def initialize(self):
        self.rsi = bt.indicators.RSI_SMA(
            self.data.close, 
            period=self.params.rsi_period
        )

    def generate_signals(self):
        # Implement abstract method
        if not self.position:
            if self.rsi < self.params.lower_threshold:
                return {'action': 'BUY'}
        else:
            if self.rsi > self.params.upper_threshold:
                return {'action': 'SELL'}
        return None

    def next(self):
        super().next()
