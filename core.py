import numpy as np
import pandas as pd
from scipy.optimize import newton
from datetime import date

class Bond:
    def __init__(self, settlement_date, maturity_date, coupon_rate, face_value=100, redemption=100, frequency=2):
        """
        Initialize a Bond object with date-based logic.
        
        :param settlement_date: Settlement date (datetime.date)
        :param maturity_date: Maturity date (datetime.date)
        :param coupon_rate: Annual coupon rate (decimal, e.g., 0.05 for 5%)
        :param face_value: Face value of the bond (Notional for coupon calc)
        :param redemption: Redemption value paid at maturity (usually same as face_value)
        :param frequency: Coupon payments per year
        """
        self.settlement_date = pd.to_datetime(settlement_date)
        self.maturity_date = pd.to_datetime(maturity_date)
        self.coupon_rate = coupon_rate
        self.face_value = face_value
        self.redemption = redemption
        self.frequency = frequency
        
        if self.settlement_date >= self.maturity_date:
            raise ValueError("Settlement date must be before maturity date.")

        # Generate cash flow dates
        # We work backwards from maturity
        dates = []
        current_date = self.maturity_date
        while current_date > self.settlement_date:
            dates.append(current_date)
            # Move back by 12/frequency months
            # Using pd.DateOffset for accurate month handling
            months = int(12 / frequency)
            current_date = current_date - pd.DateOffset(months=months)
        
        self.cash_flow_dates = sorted(dates)
        self.num_cash_flows = len(self.cash_flow_dates)
        
        # Calculate time to cash flows in years (Act/365)
        self.time_periods = np.array([(d - self.settlement_date).days / 365.0 for d in self.cash_flow_dates])
        
        # Cash flow amounts
        coupon_payment = (face_value * coupon_rate) / frequency
        self.cash_flows = np.full(self.num_cash_flows, coupon_payment)
        self.cash_flows[-1] += redemption # Add redemption to last payment

    def price(self, yield_to_maturity):
        """
        Calculate the price of the bond given a yield to maturity.
        
        :param yield_to_maturity: Annual yield to maturity (decimal)
        :return: Bond price
        """
        # Discount factors: 1 / (1 + y/f)^(t*f) ? 
        # Standard street convention often uses (1+y/f)^(n-w) where n is periods.
        # For simplicity and robustness with irregular dates, we'll use continuous or simple compounding based on time fraction.
        # Let's use standard periodic compounding adjusted for fractional years: (1 + y/f)^(t * f)
        
        # However, a more standard approach for fractional periods is:
        # P = sum( CF_i / (1 + y/f)^(w + i) ) where w is fraction of period remaining.
        # But since we calculated exact time_periods in years (t), we can use:
        # DF = 1 / (1 + y/f)^(t * f)
        
        ytm_period = yield_to_maturity / self.frequency
        discount_factors = 1 / (1 + ytm_period) ** (self.time_periods * self.frequency)
        price = np.sum(self.cash_flows * discount_factors)
        return price

    def yield_to_maturity(self, price):
        """
        Calculate the Yield to Maturity (YTM) given a price.
        """
        def price_error(y):
            return self.price(y) - price
            
        try:
            # Initial guess: coupon rate
            ytm = newton(price_error, self.coupon_rate if self.coupon_rate > 0 else 0.05)
            return ytm
        except RuntimeError:
            return np.nan

    def macaulay_duration(self, yield_to_maturity):
        """
        Calculate Macaulay Duration (in years).
        """
        ytm_period = yield_to_maturity / self.frequency
        discount_factors = 1 / (1 + ytm_period) ** (self.time_periods * self.frequency)
        
        pv_cash_flows = self.cash_flows * discount_factors
        weighted_time = np.sum(self.time_periods * pv_cash_flows) / np.sum(pv_cash_flows)
        
        return weighted_time

    def modified_duration(self, yield_to_maturity):
        """
        Calculate Modified Duration.
        """
        mac_d = self.macaulay_duration(yield_to_maturity)
        return mac_d / (1 + (yield_to_maturity / self.frequency))

    def convexity(self, yield_to_maturity):
        """
        Calculate Convexity.
        """
        ytm_period = yield_to_maturity / self.frequency
        # Convexity = (1/P) * sum( CF * t * (t + 1/f) / (1+y/f)^(t*f + 2) ) ... this is getting complex with fractional t.
        
        # Let's use the second derivative approximation or the exact formula for standard periods.
        # For general t:
        # P = sum( CF * (1+y/f)^(-t*f) )
        # dP/dy = sum( CF * (-t*f) * (1+y/f)^(-t*f - 1) * (1/f) ) = sum( -t * CF * (1+y/f)^(-t*f - 1) )
        # d2P/dy2 = sum( -t * CF * (-t*f - 1) * (1+y/f)^(-t*f - 2) * (1/f) )
        #         = sum( t * (t + 1/f) * CF / (1+y/f)^(t*f + 2) )
        
        term = self.time_periods * (self.time_periods + 1/self.frequency) * self.cash_flows / (1 + ytm_period) ** (self.time_periods * self.frequency + 2)
        sum_term = np.sum(term)
        price = self.price(yield_to_maturity)
        
        return sum_term / price

def bootstrap_yield_curve(maturities, prices, coupon_rates, face_value=100, frequency=2):
    """
    Bootstrap the zero-coupon yield curve.
    Assumes par yields or a set of bonds with varying maturities.
    
    :param maturities: List of maturities in years
    :param prices: List of bond prices
    :param coupon_rates: List of coupon rates (decimal)
    :param face_value: Face value
    :param frequency: Payment frequency
    :return: DataFrame with Maturity and ZeroRate
    """
    # Sort by maturity
    data = pd.DataFrame({
        'Maturity': maturities,
        'Price': prices,
        'Coupon': coupon_rates
    }).sort_values('Maturity')
    
    zero_rates = []
    
    for i, row in data.iterrows():
        T = row['Maturity']
        P = row['Price']
        C = row['Coupon']
        
        periods = int(T * frequency)
        coupon_payment = (face_value * C) / frequency
        
        if periods == 1:
            # Simple case for first period
            # P = (F + C_pmt) / (1 + r/f)
            # 1 + r/f = (F + C_pmt) / P
            # r = ((F + C_pmt) / P - 1) * f
            r = ((face_value + coupon_payment) / P - 1) * frequency
            zero_rates.append(r)
        else:
            # Discount previous coupons using known zero rates
            pv_coupons = 0
            for t in range(1, periods):
                # Interpolate zero rate for time t/frequency if needed
                # For simplicity here, we assume we have rates for all necessary prior periods 
                # or we use the closest available rate. 
                # A robust implementation would use interpolation.
                # Here we assume standard integer year steps for simplicity of the example,
                # or we just use the last known rate for intermediate cash flows (bootstrapping approximation).
                
                # Better approach: Linear interpolation of zero rates
                t_year = t / frequency
                
                # Find zero rate for t_year
                if t_year <= data.iloc[i-1]['Maturity']:
                     # Interpolate
                     # This is a simplified bootstrap.
                     # For a robust tool, we'd need a proper interpolation function.
                     # Let's assume we are given standard tenors (1y, 2y, 3y...)
                     # and we just use the rate corresponding to that maturity.
                     pass
            
            # For this MVP, let's implement a standard recursive solver
            # Sum(C / (1+z_t/f)^t) + (F+C)/(1+z_T/f)^T = P
            
            # Calculate PV of coupons using already calculated zero rates
            # We need a function to get zero rate at any time t
            
            def get_zero_rate(t_req, known_maturities, known_rates):
                if t_req <= known_maturities[0]:
                    return known_rates[0]
                return np.interp(t_req, known_maturities, known_rates)

            pv_coupons = 0
            current_known_maturities = data['Maturity'].iloc[:len(zero_rates)].values
            current_known_rates = np.array(zero_rates)
            
            if len(zero_rates) > 0:
                for t in range(1, periods):
                    t_time = t / frequency
                    z_rate = get_zero_rate(t_time, current_known_maturities, current_known_rates)
                    pv_coupons += coupon_payment / (1 + z_rate/frequency)**t
            
            # P = pv_coupons + (F + C_pmt) / (1 + r/f)^periods
            # P - pv_coupons = (F + C_pmt) / (1 + r/f)^periods
            # (1 + r/f)^periods = (F + C_pmt) / (P - pv_coupons)
            # 1 + r/f = ((F + C_pmt) / (P - pv_coupons))^(1/periods)
            # r = (((F + C_pmt) / (P - pv_coupons))^(1/periods) - 1) * f
            
            remaining_val = P - pv_coupons
            if remaining_val <= 0:
                 # Fallback or error if price is too low (arbitrage violation)
                 r = np.nan 
            else:
                r = (((face_value + coupon_payment) / remaining_val)**(1/periods) - 1) * frequency
            
            zero_rates.append(r)

    data['ZeroRate'] = zero_rates
    return data
