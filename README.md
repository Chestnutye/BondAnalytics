# Bond Analytics Tool

## Overview
This project is a specialized Bond Analytics Tool designed to assist with **Financial Modeling coursework**. It provides a more intuitive, powerful, and visual alternative to traditional Excel-based analysis.

While Excel functions like `YIELD` and `DURATION` are capable of basic calculations, this tool is optimized for visualization, complex model construction, and presentation convenience.

## Key Features

### 1. Interactive Visualization
- **Non-Linear Sensitivity**: Visualize **Convexity** and other non-linear relationships between Price and Yield through interactive Plotly charts.
- **Dynamic Exploration**: Zoom, pan, and hover over data points to explore the analytics in real-time, offering a significant upgrade over static Excel charts.

### 2. Built-in Term Structure Analysis
- **One-Click Bootstrapping**: Automatically constructs a **Zero-Coupon Yield Curve** from a set of coupon-bearing benchmark bonds.
- **No Complex Setup**: Eliminates the need for Excel Solver or complex VBA scripts to perform bootstrapping.

### 3. Presentation Ready
- **High-Quality Charts**: Generate professional-grade charts that are easy to screenshot and annotate for papers or presentations.
- **Clean Interface**: A distraction-free Streamlit interface that is perfect for live demos.

## Why Streamlit?
This project is built using **Streamlit**, a modern open-source Python framework designed for creating data apps.
- **Interactive**: It turns data scripts into shareable web apps in minutes, allowing for real-time interaction with the model without needing to know HTML/CSS/JavaScript.
- **Python-Native**: The entire logic is written in Python, ensuring that the financial models (using `numpy`, `pandas`, `scipy`) are directly integrated into the UI.
- **Reproducible**: Unlike Excel, where logic is hidden in cells, Streamlit apps are code-based, making the analysis transparent, version-controllable, and reproducible.

## Functionality

- **Single Bond Valuation & Risk**:
    - Calculate **Price** and **Yield to Maturity (YTM)**.
    - Compute key risk metrics: **Macaulay Duration**, **Modified Duration**, and **Convexity**.
    - Support for precise date handling (Settlement vs. Maturity) and custom Redemption values.
- **Term Structure Analysis**:
    - Input benchmark bond data to derive and plot the Zero-Coupon Yield Curve.
- **Batch Analysis**:
    - Upload Excel files for batch processing of multiple bonds.
    - Automatically generate distribution plots for Yields and Durations.

## Project Structure

```
bond_analytics/
├── app.py              # Main Streamlit application
├── core.py             # Core financial logic and Bond class
├── examples/           # Example Excel files for batch analysis
│   └── bond_analysis_template.xlsx
├── scripts/            # Utility scripts
│   └── generate_test_excel.py
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Quick Start

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Usage
- **Manual Calculation**: Use the sidebar to input bond parameters and see real-time results.
- **Batch Analysis**: Navigate to the "Batch Analysis" tab and upload the template from `examples/bond_analysis_template.xlsx`.

---
*Created for Financial Modeling Coursework.*
