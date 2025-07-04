# Backtesting Library Documentation

This library provides tools for backtesting trading strategies using historical data. It includes functionality for simulating trades, calculating technical indicators, and evaluating strategy performance.

> ⚠️ **License Notice**  
> This version is currently free to use **for personal and non-commercial purposes only**.  
> All rights are reserved. We may change license terms or revoke access to this library at any time, without prior notice.  
> Redistribution, sublicensing, or commercial usage of any part of this software is strictly prohibited unless a separate license is granted.  
> See the [LICENSE](LICENSE) file for full details.

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Simulation](#simulation)
4. [Custom Strategies](#custom-strategies)
5. [Troubleshooting](#troubleshooting)
6. [License](#license)

<a name="installation"></a>
## 1. Installation

Install the library:
- **From GitHub:**
  ```sh
  pip install git+https://github.com/stilllove1511/back-testing-lib.git
  ```

<a name="getting-started"></a>
## 2. Getting Started

Here's a minimal example to get you started:

```python
import pandas as pd
from math import floor
import flexbt as bt

# Prepare your DataFrame (example)
data = {
    "t": pd.date_range(start="2023-01-01", periods=10, freq="D"),
    "c": [1000, 1002, 1001, 1003, 1004, 1005, 1006, 1003, 1008, 1002],
    "Order": [0, 1, 0, -1, 0, 0, 0, 0, 0, 0],
}
df = pd.DataFrame(data)

# Create a Simulator instance
sim = bt.Simulator(df)

# Run the simulation
result = sim.simulate(
    order_column="Order",
    portfolio_column="Portfolio",
    initial_cash=1000.0,
    stop_loss=0,
    lot_calculator=lambda portfolio: floor(portfolio / 900) * 0.01,
)

print(result[["t", "c", "Order", "Portfolio"]])
```

<a name="simulation"></a>
## 3. Simulation

To simulate trading strategies, use the `Simulator` class. Here's an example:

```python
from math import floor
import flexbt as bt

# Custom Simulator with conditions for opening, closing, and continuing trades
class CustomSimulator(bt.Simulator):
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
```

<a name="custom-strategies"></a>
## 4. Custom Strategies

You can subclass `bt.Simulator` to override trading logic for more advanced strategies. For example:

```python
import flexbt as bt

class MyStrategy(bt.Simulator):
    def should_open_position(self, i: int, order_column: str, portfolio_column: str) -> bool:
        # Custom logic for opening a position
        pass

    def should_close_position(self, i: int, order_column: str, portfolio_column: str) -> bool:
        # Custom logic for closing a position
        pass
```

<a name="troubleshooting"></a>
## 5. Troubleshooting

- **Common Issues**
  - If you encounter issues, first check the [FAQ](faq.md) for common problems and solutions.
  - Ensure your data is correctly formatted and contains no missing values for the used columns.

- **Debugging Tips**
  - Use print statements or logging to inspect values and flow of execution in your strategy methods.
  - Simplify your strategy to the most basic form to isolate the problem, then gradually add complexity.

<a name="license"></a>
## 6. License

This software is licensed for personal, non-commercial use only.  
See the [LICENSE](LICENSE) file for detailed terms.
