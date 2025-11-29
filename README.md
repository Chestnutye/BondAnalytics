# 📊 Bond Analytics Tool

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> A specialized, interactive financial modeling tool designed for my Financial Modeling Coursework.

---

## 📖 Overview

This project is a **Bond Analytics Tool** developed to assist with **Financial Modeling coursework**. It serves as a modern, visual alternative to traditional Excel spreadsheets.

While Excel functions like `YIELD` and `DURATION` handle basic calculations, this tool excels in **visualization**, **complex model construction**, and **presentation readiness**.

## ✨ Key Features

### 1. 📈 Interactive Visualization
*   **Non-Linear Sensitivity**: Visualize **Convexity** and other non-linear relationships between Price and Yield through interactive Plotly charts.
*   **Dynamic Exploration**: Zoom, pan, and hover over data points to explore analytics in real-time.

### 2. 🏗️ Built-in Term Structure Analysis
*   **One-Click Bootstrapping**: Automatically constructs a **Zero-Coupon Yield Curve** from a set of coupon-bearing benchmark bonds.
*   **Algorithm Driven**: Uses the bootstrapping method internally, eliminating the need for Excel Solver or VBA.

### 3. 🚀 Why Streamlit?
Built with **Streamlit**, a Python-native framework for data apps:
*   **Transparent**: Logic is written in open-source Python (`numpy`, `pandas`, `scipy`), not hidden in cell formulas.
*   **Reproducible**: Version-controllable code ensures consistent results.
*   **Interactive**: Turns static models into dynamic web applications.

## 🛠️ Functionality

| Feature | Description |
| :--- | :--- |
| **Valuation** | Calculate Price & YTM with precise date handling (Settlement vs Maturity). |
| **Risk Metrics** | Compute Macaulay Duration, Modified Duration, and Convexity. |
| **Term Structure** | Bootstrap Zero-Coupon Yield Curves from benchmark bonds. |
| **Batch Analysis** | Upload Excel files (`.xlsx`) for bulk processing and visualization. |

## 📂 Project Structure

```bash
bond_analytics/
├── app.py                      # 📱 Main Streamlit application
├── core.py                     # 🧠 Core financial logic (Bond class)
├── test_core.py                # 🧪 Unit tests
├── requirements.txt            # 📦 Dependencies
├── README.md                   # 📄 Documentation
├── LICENSE                     # ⚖️ MIT License
├── examples/                   # 📂 Example data files
│   ├── README.md               # 📖 Examples documentation
│   ├── bond_analysis_template.xlsx       # Basic bond scenarios
│   ├── corporate_bonds_example.xlsx      # Corporate bonds
│   ├── term_structure_example.xlsx       # Yield curve data
└── scripts/                    # 🛠️ Utility scripts
    ├── generate_test_excel.py            # Generate basic template
    ├── generate_corporate_bonds.py       # Generate corporate bonds
    └── generate_term_structure.py        # Generate term structure data
```

## 🚀 Quick Start

### Prerequisites
*   Python 3.8+

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Chestnutye/BondAnalytics.git
    cd BondAnalytics
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app**
    ```bash
    streamlit run app.py
    ```

## 📊 Usage Guide

### Manual Calculation
Use the sidebar to input bond parameters. Results update in real-time.

### Batch Analysis
1.  Navigate to the **Batch Analysis** tab.
2.  Upload a formatted Excel file (see `examples/bond_analysis_template.xlsx`).
3.  View generated **Yield Curves** and **Duration Plots**.

## 🔧 Maintenance

### Clearing Cache
Python automatically generates bytecode cache files (`__pycache__/`) to improve performance. If you encounter unexpected behavior or want to ensure you're running the latest code, clear the cache:

```bash
# Remove Python cache files ( when you use the rm -rf command, please make sure to double check the path!!)
rm -rf __pycache__
```

The cache will be automatically regenerated when you run the application again.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

