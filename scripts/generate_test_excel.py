import pandas as pd
from datetime import date, timedelta

# Define a list of bond scenarios
data = [
    {
        'Description': 'Par Bond (Annual)',
        'Settlement Date': date(2023, 1, 1),
        'Maturity Date': date(2028, 1, 1),
        'Coupon Rate': 0.05,
        'Face Value': 100,
        'Redemption': 100,
        'Frequency': 1,
        'Market Price': 100.0,
        'YTM': None # Calculate YTM (should be 5%)
    },
    {
        'Description': 'Premium Bond (Semi-Annual)',
        'Settlement Date': date(2023, 1, 1),
        'Maturity Date': date(2026, 1, 1),
        'Coupon Rate': 0.08, # High coupon
        'Face Value': 100,
        'Redemption': 100,
        'Frequency': 2,
        'Market Price': 105.0,
        'YTM': None # Calculate YTM
    },
    {
        'Description': 'Discount Bond (Quarterly)',
        'Settlement Date': date(2023, 1, 1),
        'Maturity Date': date(2030, 1, 1),
        'Coupon Rate': 0.02, # Low coupon
        'Face Value': 100,
        'Redemption': 100,
        'Frequency': 4,
        'Market Price': None,
        'YTM': 0.045 # Calculate Price
    },
    {
        'Description': 'Zero Coupon Bond',
        'Settlement Date': date(2023, 1, 1),
        'Maturity Date': date(2033, 1, 1),
        'Coupon Rate': 0.00,
        'Face Value': 100,
        'Redemption': 100,
        'Frequency': 1,
        'Market Price': 60.0,
        'YTM': None # Calculate YTM
    },
    {
        'Description': 'Redemption Premium',
        'Settlement Date': date(2023, 1, 1),
        'Maturity Date': date(2025, 1, 1),
        'Coupon Rate': 0.05,
        'Face Value': 100,
        'Redemption': 110, # Redeem at 110
        'Frequency': 2,
        'Market Price': None,
        'YTM': 0.05 # Calculate Price
    }
]

df = pd.DataFrame(data)
# Reorder columns to put Description first if not already
cols = ['Description', 'Settlement Date', 'Maturity Date', 'Coupon Rate', 'Face Value', 'Redemption', 'Frequency', 'Market Price', 'YTM']
df = df[cols]

filename = 'bond_analysis_template.xlsx'
df.to_excel(filename, index=False)
print(f"Created {filename}")
