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
