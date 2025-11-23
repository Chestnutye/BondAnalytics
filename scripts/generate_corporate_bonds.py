import pandas as pd
from datetime import date

# Corporate Bonds Example - Various credit ratings and maturities
data = [
    {
        'Description': 'AAA Corporate 5Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2029, 1, 1),
        'Coupon Rate': 0.045,
        'Face Value': 1000,
        'Redemption': 1000,
        'Frequency': 2,
        'Market Price': 1015.50,
        'YTM': None
    },
    {
        'Description': 'AA Corporate 10Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2034, 1, 1),
        'Coupon Rate': 0.055,
        'Face Value': 1000,
        'Redemption': 1000,
        'Frequency': 2,
        'Market Price': None,
        'YTM': 0.052
    },
    {
        'Description': 'BBB Corporate 7Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2031, 1, 1),
        'Coupon Rate': 0.065,
        'Face Value': 1000,
        'Redemption': 1000,
        'Frequency': 2,
        'Market Price': 1050.00,
        'YTM': None
    },
    {
        'Description': 'High Yield 5Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2029, 1, 1),
        'Coupon Rate': 0.085,
        'Face Value': 1000,
        'Redemption': 1000,
        'Frequency': 2,
        'Market Price': 980.00,
        'YTM': None
    },
    {
        'Description': 'Callable Corporate 10Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2034, 1, 1),
        'Coupon Rate': 0.06,
        'Face Value': 1000,
        'Redemption': 1050,  # Call premium
        'Frequency': 2,
        'Market Price': None,
        'YTM': 0.058
    },
    {
        'Description': 'Investment Grade 3Y',
        'Settlement Date': date(2024, 1, 1),
        'Maturity Date': date(2027, 1, 1),
        'Coupon Rate': 0.04,
        'Face Value': 1000,
        'Redemption': 1000,
        'Frequency': 2,
        'Market Price': 995.00,
        'YTM': None
    }
]

df = pd.DataFrame(data)
cols = ['Description', 'Settlement Date', 'Maturity Date', 'Coupon Rate', 
        'Face Value', 'Redemption', 'Frequency', 'Market Price', 'YTM']
df = df[cols]

filename = '../examples/corporate_bonds_example.xlsx'
df.to_excel(filename, index=False)
print(f"Created {filename}")
