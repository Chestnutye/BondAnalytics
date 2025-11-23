import unittest
import numpy as np
import pandas as pd
from datetime import date, timedelta
from core import Bond

class TestBond(unittest.TestCase):
    def setUp(self):
        self.today = date.today()
        self.maturity_5y = self.today + timedelta(days=365*5)
        
    def test_price_par(self):
        # 5% coupon, 5% yield -> Price should be ~100 (ignoring slight day count diffs)
        # To be exact, we need integer years.
        settlement = date(2023, 1, 1)
        maturity = date(2028, 1, 1)
        bond = Bond(settlement, maturity, 0.05, 100, 100, 1) # Annual pay for simplicity
        price = bond.price(0.05)
        self.assertAlmostEqual(price, 100.0, places=1)

    def test_price_discount(self):
        settlement = date(2023, 1, 1)
        maturity = date(2028, 1, 1)
        bond = Bond(settlement, maturity, 0.05, 100, 100, 2)
        price = bond.price(0.06)
        self.assertLess(price, 100.0)

    def test_price_premium(self):
        settlement = date(2023, 1, 1)
        maturity = date(2028, 1, 1)
        bond = Bond(settlement, maturity, 0.05, 100, 100, 2)
        price = bond.price(0.04)
        self.assertGreater(price, 100.0)

    def test_ytm_calculation(self):
        settlement = date(2023, 1, 1)
        maturity = date(2028, 1, 1)
        bond = Bond(settlement, maturity, 0.05, 100, 100, 2)
        target_price = 95.0
        ytm = bond.yield_to_maturity(target_price)
        # Recalculate price with found YTM
        price_check = bond.price(ytm)
        self.assertAlmostEqual(price_check, target_price, places=4)

if __name__ == '__main__':
    unittest.main()
