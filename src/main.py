from math import floor
from typing import Protocol
import numpy as np
import pandas as pd

class LotCalc(Protocol):
    def __call__(self, portfolio: float) -> float: ...


class Simulator:
    def __init__(self, data: pd.DataFrame):
        self._data = data.copy()
        self._position = 0.0
        self._open_price = 0.0

    def basic_open_condition(self, i: int, order_column: str) -> bool:
        """Check if we should open a new position"""
        return self._position * self._data.at[i, order_column] >= 0

    def should_continue_trading(
        self, i: int, order_column: str, portfolio_column: str
    ) -> bool:
        """Check if trading should continue"""
        pass

    def should_close_position(
        self, i: int, order_column: str, portfolio_column: str
    ) -> bool:
        """Check if we should close the position"""
        pass

    def should_open_position(
        self, i: int, order_column: str, portfolio_column: str
    ) -> bool:
        """Check if we should open a new position"""
        return self.basic_open_condition(i, order_column)

    def simulate(
        self,
        order_column: str,
        portfolio_column: str,
        initial_cash=100.0,
        stop_loss=0.98,  # stop loss ratio
        spread=2,  # Spread in pips
        pip_per_price=10,
        usd_per_pip_per_lot=10,
        lot_calculator: LotCalc = lambda portfolio: floor(portfolio / 100) * 0.01,
    ) -> pd.DataFrame:
        """Simulate the futures trading portfolio value based on the trading signals"""
        self._data[portfolio_column] = float(initial_cash)
        portfolio_value = initial_cash
        trade_count = 0
        point_value = usd_per_pip_per_lot * pip_per_price

        def close_position():
            nonlocal portfolio_value
            portfolio_value = self._data.at[i, portfolio_column]
            self._position = 0.0

        for i in range(1, len(self._data)):
            profit_loss = (
                (self._data.at[i, "c"] - self._data.at[i - 1, "c"])
                * point_value
                * self._position
            )
            self._data.at[i, portfolio_column] = (
                self._data.at[i - 1, portfolio_column] + profit_loss
            )

            # Apply stop loss
            if self._data.at[i, portfolio_column] < stop_loss * portfolio_value:
                close_position()
                continue

            # Close position at the end of week (Friday)
            if (
                self._data.at[i, "t"].weekday() == 4
                and self._data.at[i, "t"].hour == 19
            ):
                close_position()
                continue

            if self.should_close_position(i, order_column, portfolio_column):
                close_position()
                continue

            if self.should_continue_trading(i, order_column, portfolio_column):
                continue

            if self._data.at[i, order_column] == 0:
                continue

            if self._position * self._data.at[i, order_column] < 0:
                close_position()
                continue

            if self.should_open_position(i, order_column, portfolio_column):
                add_position = (
                    lot_calculator(self._data.at[i, portfolio_column])
                    * self._data.at[i, order_column]
                    - self._position
                )
                self._open_price = self._data.at[i, "c"]

                if add_position != 0 and (self._position * add_position >= 0):
                    self._data.at[i, portfolio_column] -= (
                        spread
                        * usd_per_pip_per_lot
                        * add_position
                        * np.sign(self._data.at[i, order_column])
                    )
                    trade_count += 1

                self._position += add_position

        print(f"Number of trades for {order_column}: {trade_count}")
        return self._data