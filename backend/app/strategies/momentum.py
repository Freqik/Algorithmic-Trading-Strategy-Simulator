import backtrader as bt
from backend.app.strategies.base import StrategyBase

class MomentumStrategy(StrategyBase):
    """
    Simple Momentum Strategy.
    - Buy if Close > Close(t-period)
    - Sell if Close < Close(t-period)
    
    Parameters:
    - period (10): Lookback period
    """
    params = (
        ("momentum_period", 10),
        ("threshold", 0.0),
    )

    def initialize(self):
        # Momentum indicator: Price(t) - Price(t-n)
        self.momentum = bt.indicators.Momentum(
            self.data.close, 
            period=self.params.momentum_period
        )

    def generate_signals(self):
        # Implement abstract method
        if not self.position:
            if self.momentum > self.params.threshold:
                return {'action': 'BUY'}
        else:
            if self.momentum < -self.params.threshold:
                return {'action': 'SELL'}
        return None

    def next(self):
        super().next()
