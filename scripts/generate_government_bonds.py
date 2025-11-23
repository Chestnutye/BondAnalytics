import pandas as pd
from datetime import date

# Government Bonds Example - Treasury bonds with different maturities
data = [
    {
        'Description': 'T-Bill 6M (Zero Coupon)',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2024, 7, 1),
        'Coupon Rate': 0.00,
        'Face Value': 1000,
        'Redemption': 1000,
        'Frequency': 1,
        'Market Price': 975.00,
        'YTM': None
    },
    {
        'Description': 'T-Note 2Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2026, 1, 1),
        'Coupon Rate': 0.035,
        'Face Value': 1000,
        'Redemption': 1000,
        'Frequency': 2,
        'Market Price': None,
        'YTM': 0.038
    },
    {
        'Description': 'T-Note 5Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2029, 1, 1),
        'Coupon Rate': 0.042,
        'Face Value': 1000,
        'Redemption': 1000,
        'Frequency': 2,
        'Market Price': 1005.00,
        'YTM': None
    },
    {
        'Description': 'T-Note 10Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2034, 1, 1),
        'Coupon Rate': 0.048,
        'Face Value': 1000,
        'Redemption': 1000,
        'Frequency': 2,
        'Market Price': None,
        'YTM': 0.045
    },
    {
        'Description': 'T-Bond 20Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2044, 1, 1),
        'Coupon Rate': 0.052,
        'Face Value': 1000,
        'Redemption': 1000,
        'Frequency': 2,
        'Market Price': 1020.00,
        'YTM': None
    },
    {
        'Description': 'T-Bond 30Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2054, 1, 1),
        'Coupon Rate': 0.055,
        'Face Value': 1000,
        'Redemption': 1000,
        'Frequency': 2,
        'Market Price': None,
        'YTM': 0.053
    }
]

df = pd.DataFrame(data)
cols = ['Description', 'Settlement Date', 'Maturity Date', 'Coupon Rate', 
        'Face Value', 'Redemption', 'Frequency', 'Market Price', 'YTM']
df = df[cols]

filename = '../examples/government_bonds_example.xlsx'
df.to_excel(filename, index=False)
print(f"Created {filename}")
