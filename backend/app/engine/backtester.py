import backtrader as bt
import pandas as pd
from typing import Type, Dict, Any, List
from backend.app.strategies.base import StrategyBase
from backend.app.engine.execution import AccountAnalyzer, TradeLogger
from backend.app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Backtester:
    """
    Wrapper around Backtrader Cerebro engine.
    Configures the environment, instantiates the strategy, and executes the backtest.
    """

    def __init__(
        self, 
        strategy_cls: Type[StrategyBase], 
        data: pd.DataFrame, 
        params: Dict[str, Any],
        initial_capital: float = 100000.0,
        transaction_cost: float = 0.001,
        slippage: float = 0.0005
    ):
        self.cerebro = bt.Cerebro(runonce=False) # Disable runonce to avoid IndexError on short data/warmup
        self.strategy_cls = strategy_cls
        self.data = data
        self.params = params
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost
        self.slippage = slippage

    def run(self):
        """
        Runs the backtest.
        Returns a dictionary containing the equity curve, trades, and final stats.
        Handles inadequate data length or strategy errors gracefully.
        """
        try:
            # 0. Pre-validation
            if len(self.data) < 5:
                # Arbitrary small number, but if < 5, most stats meaningless.
                # Backtrader might still run but produce empty results.
                logger.warning(f"Data length ({len(self.data)}) is very short. Strategy may not trigger.")

            # 1. Setup Data Feed
            # Backtrader uses its own data feed structure.
            # We assume data is a pandas DataFrame with datetime index.
            data_feed = bt.feeds.PandasData(dataname=self.data)
            self.cerebro.adddata(data_feed)

            # 2. Setup Broker (Cash, Commission, Slippage)
            self.cerebro.broker.setcash(self.initial_capital)
            self.cerebro.broker.setcommission(commission=self.transaction_cost)
            
            # Slippage: Percentage based (0.0005 = 5 bps)
            self.cerebro.broker.set_slippage_perc(perc=self.slippage)

            # 3. Add Strategy
            self.cerebro.addstrategy(self.strategy_cls, **self.params)

            # 4. Add Analyzers
            # We attach our custom analyzers for strict accounting
            self.cerebro.addanalyzer(AccountAnalyzer, _name='account')
            self.cerebro.addanalyzer(TradeLogger, _name='trades')
            
            # 5. Run
            logger.info(f"Starting Backtest with Capital: {self.initial_capital}")
            
            # Use standard execution (runonce=False set in init)
            # This ensures next() is called step-by-step, avoiding array assignment errors in vectorized indicators check.
            results = self.cerebro.run()
            
            if not results:
                logger.warning("Backtest finished but no strategy instance returned.")
                return {
                    "equity_curve": [],
                    "trades": [],
                    "final_value": self.initial_capital
                }

            max_strat = results[0]

            # 6. Extract Results
            account_data = max_strat.analyzers.account.get_analysis()
            trade_data = max_strat.analyzers.trades.get_analysis()

            return {
                "equity_curve": account_data.get('equity_curve', []),
                "trades": trade_data.get('trades', []),
                "final_value": self.cerebro.broker.getvalue()
            }

        except IndexError as e:
            logger.error(f"Backtrader Index Error (likely insufficient data for indicators): {e}")
            # Return empty results implies "No trades possible" rather than 500
            return {
                "equity_curve": [],
                "trades": [],
                "final_value": self.initial_capital
            }
        except Exception as e:
            logger.error(f"Critical Error in Backtester.run: {e}")
            raise e
