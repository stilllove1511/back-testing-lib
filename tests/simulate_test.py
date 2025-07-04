# Copyright (c) 2025 CungUng. All rights reserved.
# This file is licensed for personal, non-commercial use only.
from math import floor
import unittest
import pandas as pd
from flexbt.main import Simulator


class TestSimulatePortfolioStaticLotSizeMode(unittest.TestCase):
    def setUp(self):
        # Tạo DataFrame mẫu để test
        self.closePrices = [
            1000,
            1002,
            1001,
            1003,
            1004,
            1005,
            1006,
            1003,
            1008,
            1002,
            1003,
            1005,
            1010,
            1008,
            1005,
            1017,
            1011,
            1010,
            1009,
            1012,
        ]
        data = {
            "t": pd.date_range(
                start="2023-01-01", periods=len(self.closePrices), freq="D"
            ),
            "c": self.closePrices,
        }
        self.df = pd.DataFrame(data)

    def test_custom_simulator(self):
        import numpy as np
        # CustomSimulator as before
        class CustomSimulator(Simulator):
            def should_continue_trading(self, i: int, order_column: str, portfolio_column: str) -> bool:
                if self._data.at[i, "t"].hour == 12 and self._data.at[i, "t"].minute >= 15:
                    return True
                if 13 <= self._data.at[i, "t"].hour <= 15:
                    return True
                return False

            def should_open_position(self, i: int, order_column: str, portfolio_column: str) -> bool:
                return (
                    self.basic_open_condition(i, order_column=order_column)
                    and self._data.at[i, order_column] == 1
                )

            def should_close_position(self, i: int, order_column: str, portfolio_column: str) -> bool:
                if self._data.at[i, "t"].hour == 12 and self._data.at[i, "t"].minute == 10:
                    return True
                if np.sign(self._position) * (self._data.at[i, "c"] - self._open_price) >= 5:
                    return True
                return False

        # More complex order signal: alternate buy/sell, some holds, and a late buy
        order_sma = [0, 1, 0, -1, 1, 0, 0, -1, 1, 0, 0, 1, -1, 0, 1, 0, -1, 1, 0, 0]
        self.df["Order_sma"] = order_sma + [0] * (len(self.df) - len(order_sma))

        simulator = CustomSimulator(self.df)
        df_result = simulator.simulate(
            order_column="Order_sma",
            portfolio_column="Portfolio_sma",
            initial_cash=1000.0,
            stop_loss=0,
            lot_calculator=lambda portfolio: floor(portfolio / 100) * 0.01,
        )

        # Check that the portfolio column exists and has the correct length
        self.assertIn("Portfolio_sma", df_result.columns)
        self.assertEqual(len(df_result), len(self.df))

        # Expectation: portfolio should change at trade points, and at least one close by price jump
        # These values are for illustration; update as needed for your logic
        expected_portfolio = [
            1000.0,  # 0: no trade
            998.0,   # 1: buy (small lot)
            988.0,   # 2: hold
            1008.0,  # 3: sell (close buy, open sell)
            1006.0,  # 4: buy (close sell, open buy)
            1016.0,  # 5: hold
            1026.0,  # 6: hold
            996.0,   # 7: sell (close buy, open sell)
            994.2,   # 8: buy (close sell, open buy)
            940.2,   # 9: hold
            949.2,   # 10: hold
            967.2,   # 11: buy (open new buy)
            1012.2,  # 12: sell (close buy, open sell)
            1012.2,  # 13: hold
            1010.2,  # 14: buy (close sell, open buy)
            1130.2,  # 15: hold
            1130.2,  # 16: sell (close buy, open sell)
            1128.0,  # 17: buy (close sell, open buy)
            1117.0,  # 18: hold
            1150.0,  # 19: hold
        ]
        for i, expected in enumerate(expected_portfolio):
            self.assertAlmostEqual(df_result["Portfolio_sma"].iloc[i], expected, places=2)

    def test_simulate_portfolio(self):
        order_base = [0, 1, 0, -1, 0, 0, 0, 0, 0, 0]
        self.df["Order_base"] = order_base + [0] * (len(self.df) - len(order_base))
        # Gọi hàm simulate_portfolio
        df = Simulator(self.df).simulate(
            order_column="Order_base",
            portfolio_column="Portfolio_base",
            initial_cash=1000.0,
            spread=2,
            pip_per_price=10,
            usd_per_pip_per_lot=10,
            stop_loss=0,
            lot_calculator=lambda portfolio: floor(portfolio / 900) * 0.01,
        )

        # Kiểm tra portfolio tại các thời điểm
        expected_values = [
            1000.0,
            999.8,
            998.8,
            1000.8,
            1000.8,
            1000.8,
            1000.8,
            1000.8,
            1000.8,
            1000.8,
        ]
        for i, expected in enumerate(expected_values):
            self.assertAlmostEqual(df["Portfolio_base"].iloc[i], expected)

    def test_simulate_portfolio_alternating_orders(self):
        order_alternating = [0, -1, 0, 1, 0, 1, -1, 0, 0, 0]
        self.df["Order_alternating"] = order_alternating + [0] * (
            len(self.df) - len(order_alternating)
        )
        # Gọi hàm simulate_portfolio
        df = Simulator(self.df).simulate(
            order_column="Order_alternating",
            portfolio_column="Portfolio_alternating",
            initial_cash=1000.0,
            spread=2,
            pip_per_price=10,
            usd_per_pip_per_lot=10,
            stop_loss=0,
            lot_calculator=lambda portfolio: floor(portfolio / 900) * 0.01,
        )

        # Kiểm tra portfolio tại các thời điểm
        expected_values = [
            1000.0,
            999.8,
            1000.8,
            998.8,
            998.8,
            998.6,
            999.6,
            999.6,
            999.6,
            999.6,
        ]
        for i, expected in enumerate(expected_values):
            self.assertAlmostEqual(df["Portfolio_alternating"].iloc[i], expected)

    def test_simulate_portfolio_multiple_buys(self):
        order_buy_many = [0, 1, 1, 1, -1, 0, 0, 0, 0, 0]
        self.df["Order_buy_many"] = order_buy_many + [0] * (
            len(self.df) - len(order_buy_many)
        )
        # Gọi hàm simulate_portfolio
        df = Simulator(self.df).simulate(
            order_column="Order_buy_many",
            portfolio_column="Portfolio_buy_many",
            initial_cash=1000.0,
            spread=2,
            pip_per_price=10,
            usd_per_pip_per_lot=10,
            stop_loss=0,
            lot_calculator=lambda portfolio: floor(portfolio / 900) * 0.01,
        )

        # Kiểm tra portfolio tại các thời điểm
        expected_values = [
            1000.0,
            999.8,
            998.8,
            1000.8,
            1001.8,
            1001.8,
            1001.8,
            1001.8,
            1001.8,
            1001.8,
        ]
        for i, expected in enumerate(expected_values):
            self.assertAlmostEqual(df["Portfolio_buy_many"].iloc[i], expected)

    def test_simulate_portfolio_multiple_sells(self):
        order_sell_many = [0, -1, -1, -1, 1, 0, 0, 0, 0, 0]
        self.df["Order_sell_many"] = order_sell_many + [0] * (
            len(self.df) - len(order_sell_many)
        )
        # Gọi hàm simulate_portfolio
        df = Simulator(self.df).simulate(
            order_column="Order_sell_many",
            portfolio_column="Portfolio_sell_many",
            initial_cash=1000.0,
            spread=2,
            pip_per_price=10,
            usd_per_pip_per_lot=10,
            stop_loss=0,
            lot_calculator=lambda portfolio: floor(portfolio / 900) * 0.01,
        )

        # Kiểm tra portfolio tại các thời điểm
        expected_values = [
            1000.0,
            999.8,
            1000.8,
            998.8,
            997.8,
            997.8,
            997.8,
            997.8,
            997.8,
            997.8,
        ]
        for i, expected in enumerate(expected_values):
            self.assertAlmostEqual(df["Portfolio_sell_many"].iloc[i], expected)

    def test_simulate_portfolio_single_multiple_buys_sells_alternating(self):
        order_compilation = [
            0,
            1,
            1,
            0,
            -1,
            -1,
            1,
            -1,
            -1,
            1,
            -1,
            1,
            0,
            1,
            -1,
            -1,
            0,
            0,
            1,
            0,
        ]
        self.df["Order_compilation"] = order_compilation + [0] * (
            len(self.df) - len(order_compilation)
        )
        # Gọi hàm simulate_portfolio
        df = Simulator(self.df).simulate(
            order_column="Order_compilation",
            portfolio_column="Portfolio_compilation",
            initial_cash=1000.0,
            spread=2,
            pip_per_price=10,
            usd_per_pip_per_lot=10,
            stop_loss=0,
            lot_calculator=lambda portfolio: floor(portfolio / 900) * 0.01,
        )

        print("czxczxz", df["Portfolio_compilation"].values)

        # Kiểm tra portfolio tại các thời điểm
        expected_values = [
            1000.0,
            999.8,
            998.8,
            1000.8,
            1001.8,
            1001.6,
            1000.6,
            1000.4,
            995.4,
            1001.4,
            1001.2,
            999.2,
            999.2,
            999,
            996,
            995.8,
            1001.8,
            1002.8,
            1003.8,
            1003.8,
        ]
        for i, expected in enumerate(expected_values):
            self.assertAlmostEqual(df["Portfolio_compilation"].iloc[i], expected)

    def test_simulate_portfolio_single_multiple_buys_sells_alternating_no_spread(self):
        order_compilation = [
            0,
            1,
            1,
            0,
            -1,
            -1,
            1,
            -1,
            -1,
            1,
            -1,
            1,
            0,
            1,
            -1,
            -1,
            0,
            0,
            1,
            0,
        ]
        self.df["Order_compilation"] = order_compilation + [0] * (
            len(self.df) - len(order_compilation)
        )
        # Gọi hàm simulate_portfolio
        df = Simulator(self.df).simulate(
            order_column="Order_compilation",
            portfolio_column="Portfolio_compilation",
            initial_cash=1000.0,
            spread=0,
            pip_per_price=10,
            usd_per_pip_per_lot=10,
            stop_loss=0,
            lot_calculator=lambda portfolio: floor(portfolio / 900) * 0.01,
        )

        print("czxczxz", df["Portfolio_compilation"].values)

        # Kiểm tra portfolio tại các thời điểm
        expected_values = [
            1000.0,
            1000.0,
            999,
            1001,
            1002,
            1002,
            1001,
            1001,
            996,
            1002,
            1002,
            1000,
            1000,
            1000,
            997,
            997,
            1003,
            1004,
            1005,
            1005,
        ]
        for i, expected in enumerate(expected_values):
            self.assertAlmostEqual(df["Portfolio_compilation"].iloc[i], expected)

    def test_simulate_portfolio_weekend_cutoff(self):
        data = {
            "t": pd.date_range(
                start="2023-01-01 19:00", periods=len(self.closePrices), freq="D"
            ),
            "c": self.closePrices,
        }
        df = pd.DataFrame(data)

        order_weekend_cutoff = [
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
        df["Order_weekend_cutoff"] = order_weekend_cutoff + [0] * (
            len(df) - len(order_weekend_cutoff)
        )

        # Gọi hàm simulate_portfolio với logic cắt lệnh vào cuối tuần
        df = Simulator(df).simulate(
            order_column="Order_weekend_cutoff",
            portfolio_column="Portfolio_weekend_cutoff",
            initial_cash=1000.0,
            spread=0,
            pip_per_price=10,
            usd_per_pip_per_lot=10,
            stop_loss=0,
            lot_calculator=lambda portfolio: floor(portfolio / 900) * 0.01,
        )

        # Kiểm tra portfolio tại các thời điểm
        expected_values = [
            1000.0,
            1000.0,
            999.0,
            1001.0,
            1002.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
            1003.0,
        ]
        for i, expected in enumerate(expected_values):
            self.assertAlmostEqual(df["Portfolio_weekend_cutoff"].iloc[i], expected)


if __name__ == "__main__":
    unittest.main()
