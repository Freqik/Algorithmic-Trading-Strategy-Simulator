import backtrader as bt
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class AccountAnalyzer(bt.Analyzer):
    """
    Tracks daily portfolio value (Equity Curve).
    Includes Cash and Total Value (realized + unrealized).
    """
    
    def __init__(self):
        self.equity_curve = []

    def next(self):
        # Called every bar
        self.capture_state()

    def capture_state(self):
        """
        Records the current state of the portfolio.
        Safe access to date and values.
        """
        if not len(self.strategy):
            return

        try:
            # backtrader dates are floats, convert to datetime
            dt = self.strategy.datetime.date()
            value = self.strategy.broker.getvalue()
            cash = self.strategy.broker.getcash()
            
            self.equity_curve.append({
                "date": dt,
                "equity": value,
                "cash": cash
            })
        except Exception as e:
            logger.error(f"Error capturing account state: {e}")

    def get_analysis(self):
        return {
            "equity_curve": self.equity_curve
        }


class TradeLogger(bt.Analyzer):
    """
    Logs every completed trade with strict lifecycle details.
    Fixes ZeroDivisionError by avoiding division by trade.size on closed trades.
    """
    
    def __init__(self):
        self.trades = []

    def notify_trade(self, trade):
        """
        Backtrader hook called when a trade is updated or closed.
        We only care about CLOSED trades for the final log.
        """
        if trade.isclosed:
            try:
                # Safe Extraction of Trade Details
                ticker = trade.data._name if hasattr(trade.data, '_name') else "Unknown"
                
                # Dates
                entry_date = bt.num2date(trade.dtopen)
                exit_date = bt.num2date(trade.dtclose)
                
                # Prices
                # trade.price is the entry price (average).
                entry_price = trade.price
                
                # Calculate Exit Price safely
                # PnL = (Exit_Price - Entry_Price) * Size
                # But trade.size is 0 now.
                # However, the PnL was realized on the 'initial' size or 'closed' size.
                # We don't have the closed size explicitly in the 'trade' object easily if partial closures happened,
                # but assuming single-shot closure or aggregated trade:
                
                # Valid fallback: exit_price is None if we can't be sure, 
                # or simplified: since we know PnL and Entry, strictly strictly:
                # We can't divide by size=0.
                exit_price = None 

                # Metrics
                pnl = trade.pnl          # Gross PnL
                pnl_net = trade.pnlcomm  # Net PnL (after commissions)
                
                # Duration
                duration = (exit_date - entry_date).days if entry_date and exit_date else 0

                trade_record = {
                    "ticker": ticker,
                    "entry_date": entry_date,
                    "exit_date": exit_date,
                    "entry_price": entry_price,
                    "exit_price": exit_price, # Explicitly None to avoid guessing/division errors
                    "pnl": pnl,
                    "pnl_net": pnl_net,
                    "size": 0, # Closed means size is handled. We don't record 'size traded' here unless we track history.
                    "duration": duration
                }
                
                self.trades.append(trade_record)

            except Exception as e:
                logger.error(f"Error logging trade: {e}")
            
    def get_analysis(self):
        return {
            "trades": self.trades
        }
