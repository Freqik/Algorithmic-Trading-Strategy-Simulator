import backtrader as bt
from backend.app.strategies.base import StrategyBase

class MaCrossover(StrategyBase):
    """
    Moving Average Crossover Strategy.
    Buy when Short MA crosses above Long MA.
    Sell when Short MA crosses below Long MA.
    """
    
    # Parameters definition with defaults
    params = (
        ('short_window', 20),
        ('long_window', 50),
    )

    def initialize(self):
        """
        Initialize the moving averages.
        """
        # We use Backtrader's built-in indicators. 
        # They automatically register and calculate on 'next'.
        self.sma_short = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.short_window
        )
        self.sma_long = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.long_window
        )
        
        # CrossOver indicator returns 1 if arg0 > arg1, -1 if arg0 < arg1
        self.crossover = bt.indicators.CrossOver(self.sma_short, self.sma_long)

    def generate_signals(self):
        """
        Check for crossover.
        """
        # Backtrader indicators are accessed like arrays (0 is current)
        
        if self.crossover > 0:
            return {'action': 'BUY'}
        elif self.crossover < 0:
            return {'action': 'SELL'}
        
        return None
