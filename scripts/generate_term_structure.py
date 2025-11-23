import pandas as pd
from datetime import date

# Term Structure Example - Benchmark bonds for bootstrapping yield curve
# These bonds are designed to demonstrate the bootstrapping method
data = [
    {
        'Description': 'Benchmark 6M',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2024, 7, 1),
        'Coupon Rate': 0.00,  # Zero coupon for short term
        'Face Value': 100,
        'Redemption': 100,
        'Frequency': 2,
        'Market Price': 98.00,
        'YTM': None
    },
    {
        'Description': 'Benchmark 1Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2025, 1, 1),
        'Coupon Rate': 0.035,
        'Face Value': 100,
        'Redemption': 100,
        'Frequency': 2,
        'Market Price': 100.50,
        'YTM': None
    },
    {
        'Description': 'Benchmark 2Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2026, 1, 1),
        'Coupon Rate': 0.04,
        'Face Value': 100,
        'Redemption': 100,
        'Frequency': 2,
        'Market Price': 101.00,
        'YTM': None
    },
    {
        'Description': 'Benchmark 3Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2027, 1, 1),
        'Coupon Rate': 0.045,
        'Face Value': 100,
        'Redemption': 100,
        'Frequency': 2,
        'Market Price': 102.00,
        'YTM': None
    },
    {
        'Description': 'Benchmark 5Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2029, 1, 1),
        'Coupon Rate': 0.05,
        'Face Value': 100,
        'Redemption': 100,
        'Frequency': 2,
        'Market Price': 103.50,
        'YTM': None
    },
    {
        'Description': 'Benchmark 7Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2031, 1, 1),
        'Coupon Rate': 0.052,
        'Face Value': 100,
        'Redemption': 100,
        'Frequency': 2,
        'Market Price': 104.00,
        'YTM': None
    },
    {
        'Description': 'Benchmark 10Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2034, 1, 1),
        'Coupon Rate': 0.055,
        'Face Value': 100,
        'Redemption': 100,
        'Frequency': 2,
        'Market Price': 105.00,
        'YTM': None
    }
]

df = pd.DataFrame(data)
cols = ['Description', 'Settlement Date', 'Maturity Date', 'Coupon Rate', 
        'Face Value', 'Redemption', 'Frequency', 'Market Price', 'YTM']
df = df[cols]

filename = '../examples/term_structure_example.xlsx'
df.to_excel(filename, index=False)
print(f"Created {filename}")
