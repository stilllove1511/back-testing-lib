```python
from math import floor
import numpy as np
from main import Simulator
from strategy import calculate_bollinger_bands, calculate_sma

# Calculate SMA and Bollinger Bands
calculate_sma(df, 10, 30, "Order_sma")
calculate_bollinger_bands(
    df,
    order_col="Order_bb",
    window=20,
    num_std_dev=1,
)

# Custom Simulator with conditions for opening, closing, and continuing trades
class CustomSimulator(Simulator):
    def should_continue_trading(self, i: int, order_column: str, portfolio_column: str) -> bool:
        """ Check whether to continue trading """
        if self._data.at[i, "t"].hour == 12 and self._data.at[i, "t"].minute >= 15:
            return True
        if 13 <= self._data.at[i, "t"].hour <= 15:
            return True
        return False

    def should_open_position(self, i: int, order_column: str, portfolio_column: str) -> bool:
        """ Check if the conditions for opening a position are met """
        return (
            self.basic_open_condition(i, order_column=order_column)
            and self._data.at[i, order_column] == 1
        )

    def should_close_position(self, i: int, order_column: str, portfolio_column: str) -> bool:
        """ Check if the conditions for closing a position are met """
        if self._data.at[i, "t"].hour == 12 and self._data.at[i, "t"].minute == 10:
            return True
        if np.sign(self._position) * (self._data.at[i, "c"] - self._open_price) >= 5:
            return True
        return False

# Initialize the simulator
simulator = CustomSimulator(df)

# Simulate with the SMA strategy
df = simulator.simulate(
    order_column="Order_sma",
    portfolio_column="Portfolio_sma",
    initial_cash=1000.0,
    stop_loss=0,
    lot_calculator=lambda portfolio: floor(portfolio / 100) * 0.01,
)

# Simulate with the Bollinger Bands strategy
df = simulator.simulate(
    order_column="Order_bb",
    portfolio_column="Portfolio_BB",
    initial_cash=1000.0,
    stop_loss=0,
    lot_calculator=lambda portfolio: floor(portfolio / 100) * 0.01,
)
```
