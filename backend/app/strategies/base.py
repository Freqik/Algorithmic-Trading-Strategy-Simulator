import backtrader as bt
from abc import abstractmethod
import logging

logger = logging.getLogger(__name__)

class StrategyBase(bt.Strategy):
    """
    Abstract Base Class for all strategies.
    Enforces a strict interface for initialization, signal generation, and execution.
    Wraps Backtrader's functionality to meet project requirements.
    """
    
    # Define parameters structure in subclasses
    params = (
        ('name', 'basetrategey'),
    )

    def __init__(self):
        """
        Backtrader's initialization method. 
        We use this to set up indicators.
        """
        self.signals = {} # efficient signal tracking
        self.initialize()

    @abstractmethod
    def initialize(self):
        """
        Custom initialization logic (e.g., creating indicators).
        Must be implemented by subclasses.
        """
        pass

    def next(self):
        """
        Called by Backtrader on every new data bar.
        Orchestrates the lifecycle: Generate Signals -> Execute.
        """
        signal = self.generate_signals()
        
        if signal:
            self.execute_trade(signal)

    @abstractmethod
    def generate_signals(self):
        """
        Analyze markets and return a signal.
        Returns:
            dict or object: Signal details (e.g., {'action': 'BUY', 'size': 10}) or None.
        """
        pass

    def execute_trade(self, signal):
        """
        Executes a trade based on the generated signal.
        
        Args:
            signal (dict): The signal object containing 'action' (BUY/SELL).
        """
        # Default implementation using Backtrader's buy/sell
        # Subclasses can override if complex execution logic is needed
        
        size = signal.get('size', None) # If None, simpler sizers are used or full capital
        
        if signal['action'] == 'BUY':
            if not self.position:
                logger.info(f"[{self.datetime.date()}] BUY Signal executing")
                self.buy(size=size)
            
        elif signal['action'] == 'SELL':
            if self.position:
                logger.info(f"[{self.datetime.date()}] SELL Signal executing")
                self.close() # Close position clearly
                
                # If it's a short strategy, we might do self.sell() here. 
                # For this simulator, we assume Long-Only or Long-Short via 'sell' to open short?
                # User constraints didn't specify Long-Only, but typical simple strategies are.
                # 'close_positions' was requested as a specific method.

    def close_positions(self):
        """
        Force close all positions.
        """
        if self.position:
            logger.info(f"[{self.datetime.date()}] Force Closing Positions")
            self.close()

    def notify_order(self, order):
        """
        Logging order status changes.
        """
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                logger.info(f"BUY EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}")
            elif order.issell():
                logger.info(f"SELL EXECUTED, Price: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, Comm: {order.executed.comm:.2f}")
            
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            logger.warning("Order Canceled/Margin/Rejected")
