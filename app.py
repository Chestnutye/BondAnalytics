import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from core import Bond, bootstrap_yield_curve

st.set_page_config(page_title="Bond Analytics Tool", layout="wide")

st.title("Bond Analytics Tool")

tabs = st.tabs(["Valuation & Risk", "Term Structure Analysis", "Batch Analysis"])

with tabs[0]:
    st.header("Bond Valuation & Risk Analysis")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Bond Parameters")
        settlement_date = st.date_input("Settlement Date", value=pd.to_datetime("today").date())
        maturity_date = st.date_input("Maturity Date", value=pd.to_datetime("today").date() + pd.DateOffset(years=5))
        
        # Ensure dates are valid
        if settlement_date >= maturity_date:
            st.error("Error: Settlement Date must be before Maturity Date.")
            st.stop()
            
        coupon_rate = st.number_input("Coupon Rate", value=5.00, step=0.01, format="%.2f") / 100
        face_value = st.number_input("Face Value", value=100.00, step=10.00, format="%.2f")
        redemption = st.number_input("Redemption", value=100.00, step=10.00, format="%.2f", help="Amount paid at maturity.")
        frequency = st.selectbox("Frequency", options=[1, 2, 4, 12], index=1, format_func=lambda x: f"{x} per year")
        
        st.subheader("Market Data")
        calc_mode = st.radio("Calculation Mode", ["Calculate Price from YTM", "Calculate YTM from Price"])
        
        if calc_mode == "Calculate Price from YTM":
            ytm_input = st.number_input("Yield to Maturity (%)", value=5.00, step=0.01, format="%.2f") / 100
            price_input = None
        else:
            price_input = st.number_input("Price, P", value=100.00, step=0.01, format="%.2f")
            ytm_input = None

    with col2:
        try:
            bond = Bond(settlement_date, maturity_date, coupon_rate, face_value, redemption, frequency)
            
            if calc_mode == "Calculate Price from YTM":
                price = bond.price(ytm_input)
                ytm = ytm_input
                st.metric("Price, P", f"{price:.2f}")
            else:
                ytm = bond.yield_to_maturity(price_input)
                price = price_input
                if np.isnan(ytm):
                    st.error("Could not calculate YTM. Price might be invalid.")
                else:
                    st.metric("Yield to Maturity", f"{ytm*100:.2f}%")

            if not np.isnan(ytm):
                st.subheader("Risk Metrics")
                c1, c2, c3 = st.columns(3)
                mac_d = bond.macaulay_duration(ytm)
                mod_d = bond.modified_duration(ytm)
                conv = bond.convexity(ytm)
                
                c1.metric("Macaulay Duration", f"{mac_d:.2f} years")
                c2.metric("Modified Duration", f"{mod_d:.2f}")
                c3.metric("Convexity", f"{conv:.2f}")
                
                st.subheader("Price Sensitivity Analysis")
                # Generate yield range
                yields = np.linspace(max(0.001, ytm - 0.05), ytm + 0.05, 100)
                prices = [bond.price(y) for y in yields]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=yields*100, y=prices, mode='lines', name='Price-Yield Curve'))
                fig.add_trace(go.Scatter(x=[ytm*100], y=[price], mode='markers', name='Current Position', marker=dict(color='red', size=10)))
                
                fig.update_layout(
                    title="Price vs Yield",
                    xaxis_title="Yield (%)",
                    yaxis_title="Price",
                    hovermode="x unified"
                )
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error in calculation: {e}")

with tabs[1]:
    st.header("Term Structure Analysis (Bootstrapping)")
    
    st.write("Enter benchmark bonds to construct the zero-coupon yield curve.")
    
    # Example data
    default_data = pd.DataFrame({
        'Maturity (Years)': [0.5, 1.0, 1.5, 2.0, 3.0, 5.0],
        'Coupon (%)': [0.0, 0.0, 2.0, 3.0, 4.0, 5.0],
        'Price': [99.0, 97.5, 99.0, 99.5, 101.0, 102.0]
    })
    
    edited_df = st.data_editor(default_data, num_rows="dynamic")
    
    if st.button("Calculate Yield Curve"):
        try:
            maturities = edited_df['Maturity (Years)'].values
            coupons = edited_df['Coupon (%)'].values / 100
            prices = edited_df['Price'].values
            
            curve_df = bootstrap_yield_curve(maturities, prices, coupons)
            
            st.subheader("Zero-Coupon Yield Curve")
            st.dataframe(curve_df.style.format({"ZeroRate": "{:.4%}", "Coupon": "{:.2%}"}))
            
            fig_curve = go.Figure()
            fig_curve.add_trace(go.Scatter(x=curve_df['Maturity'], y=curve_df['ZeroRate']*100, mode='lines+markers', name='Zero Rate'))
            fig_curve.update_layout(
                title="Zero-Coupon Yield Curve",
                xaxis_title="Maturity (Years)",
                yaxis_title="Zero Rate (%)"
            )
            st.plotly_chart(fig_curve, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error calculating yield curve: {e}")

with tabs[2]:
    st.header("Batch Analysis")
    st.write("Upload an Excel file with bond data to perform batch calculations.")
    
    with st.expander("ℹ️ Why do I need Price or YTM?"):
        st.write("""
        The parameters in the image (**Settlement, Maturity, Coupon, Face Value, Redemption, Frequency**) define the **Cash Flows** of the bond (the promises).
        
        However, to know the bond's value, we need a market variable:
        *   **To calculate Price**: We need a discount rate (**YTM**).
        *   **To calculate YTM**: We need the current market **Price**.
        
        They are connected by the formula:
        $$ P = \\sum_{t=1}^{n} \\frac{C}{(1+y)^t} + \\frac{R}{(1+y)^n} $$
        
        Where $P$ is Price, $C$ is Coupon, $R$ is Redemption, and $y$ is Yield. You cannot solve for both $P$ and $y$ without knowing one of them.
        """)
        
    st.info("Note: To calculate YTM, your Excel file must include a 'Price' column. To calculate Price, it must include a 'YTM' column.")
    
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Preview of uploaded data:")
            st.dataframe(df.head())
            
            required_cols = ['Settlement Date', 'Maturity Date', 'Coupon Rate', 'Face Value', 'Frequency']
            if not all(col in df.columns for col in required_cols):
                st.error(f"Missing required columns. Please ensure your Excel has: {', '.join(required_cols)}")
            else:
                if st.button("Run Batch Analysis"):
                    results = []
                    for index, row in df.iterrows():
                        try:
                            # Handle optional columns with defaults
                            redemption = row.get('Redemption', 100.0)
                            
                            bond = Bond(
                                row['Settlement Date'],
                                row['Maturity Date'],
                                row['Coupon Rate'], # Assumed decimal or handle % later? Let's assume decimal as per app logic
                                row['Face Value'],
                                redemption,
                                int(row['Frequency'])
                            )
                            
                            res = row.to_dict()
                            
                            # Determine what to calculate
                            if 'Market Price' in row and pd.notnull(row['Market Price']):
                                price = row['Market Price']
                                ytm = bond.yield_to_maturity(price)
                                res['Calculated YTM'] = ytm
                            elif 'YTM' in row and pd.notnull(row['YTM']):
                                ytm = row['YTM']
                                price = bond.price(ytm)
                                res['Calculated Price'] = price
                            else:
                                ytm = np.nan
                                price = np.nan
                                
                            if not np.isnan(ytm):
                                res['Macaulay Duration'] = bond.macaulay_duration(ytm)
                                res['Modified Duration'] = bond.modified_duration(ytm)
                                res['Convexity'] = bond.convexity(ytm)
                                
                            results.append(res)
                        except Exception as e:
                            res = row.to_dict()
                            res['Error'] = str(e)
                            results.append(res)
                    
                    results_df = pd.DataFrame(results)
                    st.subheader("Results")
                    st.dataframe(results_df)
                    
                    # Sort by Maturity Date for better visualization
                    if 'Maturity Date' in results_df.columns:
                        results_df_sorted = results_df.sort_values('Maturity Date').reset_index(drop=True)
                    else:
                        results_df_sorted = results_df
                    
                    # Prepare labels (use Description if available, otherwise use index)
                    if 'Description' in results_df_sorted.columns:
                        labels = results_df_sorted['Description'].astype(str)
                    else:
                        labels = results_df_sorted.index.astype(str)
                    
                    # Visualizations
                    st.subheader("📊 Visual Analysis")
                    
                    # Create columns for better layout
                    viz_col1, viz_col2 = st.columns(2)
                    
                    with viz_col1:
                        if 'Calculated YTM' in results_df_sorted.columns:
                            # Plot Yield Curve (YTM vs Maturity Date)
                            fig_yield = go.Figure()
                            fig_yield.add_trace(go.Scatter(
                                x=results_df_sorted['Maturity Date'], 
                                y=results_df_sorted['Calculated YTM']*100, 
                                mode='lines+markers+text',
                                name='Yield',
                                text=[f"{y:.2f}%" for y in results_df_sorted['Calculated YTM']*100],
                                textposition="top center",
                                textfont=dict(size=9),
                                marker=dict(size=8),
                                line=dict(width=2)
                            ))
                            fig_yield.update_layout(
                                title="Yield vs Maturity",
                                xaxis_title="Maturity Date",
                                yaxis_title="Yield (%)",
                                hovermode="x unified",
                                showlegend=True,
                                height=400,
                                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
                                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray')
                            )
                            st.plotly_chart(fig_yield, use_container_width=True)
                        
                        if 'Macaulay Duration' in results_df_sorted.columns:
                            fig_dur = go.Figure()
                            fig_dur.add_trace(go.Scatter(
                                x=results_df_sorted['Maturity Date'], 
                                y=results_df_sorted['Macaulay Duration'], 
                                mode='lines+markers+text',
                                name='Duration',
                                text=[f"{d:.2f}" for d in results_df_sorted['Macaulay Duration']],
                                textposition="top center",
                                textfont=dict(size=9),
                                marker=dict(size=8, color='orange'),
                                line=dict(width=2, color='orange')
                            ))
                            fig_dur.update_layout(
                                title="Duration vs Maturity",
                                xaxis_title="Maturity Date",
                                yaxis_title="Duration (Years)",
                                hovermode="x unified",
                                showlegend=True,
                                height=400,
                                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
                                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray')
                            )
                            st.plotly_chart(fig_dur, use_container_width=True)
                    
                    with viz_col2:
                        if 'Calculated Price' in results_df_sorted.columns:
                            # Plot Price vs Maturity
                            fig_price = go.Figure()
                            fig_price.add_trace(go.Scatter(
                                x=results_df_sorted['Maturity Date'], 
                                y=results_df_sorted['Calculated Price'], 
                                mode='lines+markers+text',
                                name='Price',
                                text=[f"{p:.2f}" for p in results_df_sorted['Calculated Price']],
                                textposition="top center",
                                textfont=dict(size=9),
                                marker=dict(size=8, color='green'),
                                line=dict(width=2, color='green')
                            ))
                            fig_price.update_layout(
                                title="Price vs Maturity",
                                xaxis_title="Maturity Date",
                                yaxis_title="Price",
                                hovermode="x unified",
                                showlegend=True,
                                height=400,
                                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
                                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray')
                            )
                            st.plotly_chart(fig_price, use_container_width=True)
                        elif 'Market Price' in results_df_sorted.columns:
                            # Use Market Price if Calculated Price not available
                            fig_price = go.Figure()
                            fig_price.add_trace(go.Scatter(
                                x=results_df_sorted['Maturity Date'], 
                                y=results_df_sorted['Market Price'], 
                                mode='lines+markers+text',
                                name='Price',
                                text=[f"{p:.2f}" for p in results_df_sorted['Market Price']],
                                textposition="top center",
                                textfont=dict(size=9),
                                marker=dict(size=8, color='green'),
                                line=dict(width=2, color='green')
                            ))
                            fig_price.update_layout(
                                title="Price vs Maturity",
                                xaxis_title="Maturity Date",
                                yaxis_title="Price",
                                hovermode="x unified",
                                showlegend=True,
                                height=400,
                                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
                                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray')
                            )
                            st.plotly_chart(fig_price, use_container_width=True)
                        
                        if 'Convexity' in results_df_sorted.columns:
                            # Plot Convexity vs Maturity
                            fig_conv = go.Figure()
                            fig_conv.add_trace(go.Scatter(
                                x=results_df_sorted['Maturity Date'], 
                                y=results_df_sorted['Convexity'], 
                                mode='lines+markers+text',
                                name='Convexity',
                                text=[f"{c:.2f}" for c in results_df_sorted['Convexity']],
                                textposition="top center",
                                textfont=dict(size=9),
                                marker=dict(size=8, color='purple'),
                                line=dict(width=2, color='purple')
                            ))
                            fig_conv.update_layout(
                                title="Convexity vs Maturity",
                                xaxis_title="Maturity Date",
                                yaxis_title="Convexity",
                                hovermode="x unified",
                                showlegend=True,
                                height=400,
                                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
                                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray')
                            )
                            st.plotly_chart(fig_conv, use_container_width=True)

        except Exception as e:
            st.error(f"Error reading file: {e}")
