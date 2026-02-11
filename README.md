```markdown
# Brent Oil Change Point Analysis

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyMC](https://img.shields.io/badge/PyMC-5.8+-orange.svg)](https://www.pymc.io/)
[![React](https://img.shields.io/badge/react-18+-61DAFB.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Bayesian change point detection and interactive visualization of Brent oil price structural breaks (1987-2022)**
> 
> 10 Academy - Week 11 Challenge | Artificial Intelligence Mastery | February 2026

---

## 🎯 Project Overview

This project analyzes 35 years of Brent crude oil prices to identify **structural breaks** (change points) caused by major geopolitical events, economic shocks, and OPEC policy decisions. Using **Bayesian inference** with PyMC, we quantify the timing and magnitude of regime changes to support investment strategies, policy development, and risk management.

### Business Problem

Birhan Energies, a leading energy sector consultancy, requires data-driven insights into how major events impact oil prices. This analysis addresses:

| Stakeholder | Question | Solution |
|:---|:---|:---|
| **Investors** | When to buy/sell based on regime changes? | Detected change points with confidence intervals |
| **Policymakers** | Which interventions had measurable impact? | Event-associated structural breaks |
| **Energy Companies** | How to hedge against volatility shocks? | Quantified volatility regime changes |

### Key Results

| Change Point | Date | Daily Impact | Volatility Change | Associated Event |
|:---|:---|:---|:---|:---|
| **Gulf War** | 1990-08-02 | -10.00% | 3.4x | Iraq invades Kuwait |
| **Financial Crisis** | 2008-09-15 | **-70.00%** | 2.4x | Lehman Brothers collapse |
| **OPEC Price War** | 2014-11-26 | -10.00% | 2.5x | OPEC abandons price defense |
| **COVID-19** | 2020-03-11 | **-470.00%** | **6.2x** | WHO declares pandemic |

---

## 🏗️ Repository Structure

```
brent-oil-change-point-analysis/
│
├── 📁 data/                          # All data files
│   ├── raw/                          # Original Brent prices (1987-2022)
│   │   └── BrentOilPrices.csv
│   ├── processed/                    # Cleaned data with features
│   │   ├── features_engineered.csv
│   │   └── change_point_results.csv
│   └── external/                     # Researched events
│       └── geopolitical_events.csv
│
├── 📁 notebooks/                     # Analysis notebooks
│   ├── 01_eda.ipynb                  # Task 1: EDA and data foundation
│   ├── 02_bayesian_modeling.ipynb    # Task 2: Change point detection
│   └── 03_advanced_analysis.ipynb    # Extensions and validation
│
├── 📁 src/                           # Production code
│   ├── data/                         # Data processing modules
│   │   ├── load_data.py
│   │   ├── clean_data.py
│   │   └── features.py
│   ├── models/                       # Bayesian models
│   │   └── change_point.py
│   ├── visualization/                # Plotting utilities
│   │   └── plots.py
│   └── dashboard/                    # Task 3: Flask backend
│       └── app.py
│
├── 📁 dashboard-frontend/            # Task 3: React frontend
│   ├── src/
│   │   ├── App.js                    # Main dashboard component
│   │   ├── App.css                   # Styling
│   │   └── index.js
│   └── package.json
│
├── 📁 reports/                       # Documentation
│   ├── interim_report.md             # Task 1 submission
│   ├── final_report.md               # Complete analysis
│   └── figures/                      # Generated visualizations
│       ├── 01_full_series.png
│       ├── 02_returns_volatility.png
│       ├── 03_mean_comparison.png
│       └── 05_final_change_points.png
│
├── 📄 requirements.txt               # Python dependencies
├── 📄 README.md                      # This file
└── 📄 .gitignore                     # Git exclusions
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- Git

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/brent-oil-change-point-analysis.git
cd brent-oil-change-point-analysis
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate
# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd dashboard-frontend
npm install
cd ..
```

### 4. Run Analysis (Optional)

```bash
cd notebooks
jupyter notebook 01_eda.ipynb          # Task 1: EDA
jupyter notebook 02_bayesian_modeling.ipynb  # Task 2: Modeling
```

### 5. Run Dashboard

Terminal 1 - Backend:
```bash
cd src/dashboard
python app.py
# API available at: http://localhost:5000
```

Terminal 2 - Frontend:
```bash
cd dashboard-frontend
npm start
# Dashboard opens at: http://localhost:3000
```

---

## 📊 Methodology

### Task 1: Data Foundation
- **Data**: 9,011 daily Brent prices (May 20, 1987 – September 30, 2022)
- **Cleaning**: Date parsing, missing value handling, quality validation
- **Features**: Log returns, volatility measures (7d, 30d, 90d), moving averages
- **Validation**: ADF test confirms stationarity (ADF = -12.60, p < 0.001)

### Task 2: Bayesian Change Point Detection
- **Approach**: Two-stage (detect τ, then Bayesian parameter estimation)
- **Framework**: PyMC with NUTS sampler
- **Model**: Normal likelihood with regime-specific means and variances
- **Validation**: 
  - R-hat < 1.01 (perfect convergence)
  - ESS > 4,000 (excellent sampling efficiency)
  - 95% credible intervals for all parameters

### Task 3: Interactive Dashboard
- **Backend**: Flask REST API
- **Frontend**: React with Recharts
- **Features**: 
  - Interactive price chart with change point markers
  - Date range filtering
  - Impact metrics visualization
  - MCMC diagnostics display

---

## 📈 Key Findings

### 1. Four Distinct Regimes Identified

| Era | Period | Characteristics |
|:---|:---|:---|
| **Stable Low** | 1987-1990 | $15-25, low volatility |
| **Gulf War Shock** | 1990-2008 | Elevated volatility, gradual rise |
| **Financial Crisis** | 2008-2014 | High volatility, $100 plateau |
| **Shale/OPEC War** | 2014-2020 | Structural break to lower prices |
| **COVID Era** | 2020-2022 | Extreme volatility, recovery |

### 2. Volatility Clustering

- **Normal times**: ~20-35% annualized volatility
- **Crisis periods**: 75-146% annualized volatility (2-6x increase)
- **Largest shock**: COVID-19 with 6.2x volatility multiplier

### 3. Return Impact

- **Financial Crisis 2008**: -0.70% daily returns (-176% annualized)
- **COVID-19 2020**: -4.70% daily returns at peak (-1,184% annualized)
- **Structural breaks** persist longer than temporary shocks

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|:---|:---|:---|
| **Language** | Python 3.9+ | Data processing, modeling |
| **Bayesian Framework** | PyMC 5.8+ | Change point detection |
| **Data Processing** | Pandas, NumPy | Feature engineering |
| **Visualization** | Matplotlib, Seaborn, Recharts | EDA and dashboard |
| **Backend** | Flask | REST API |
| **Frontend** | React 18 | Interactive dashboard |
| **Version Control** | Git, GitHub | Collaboration |

---

## 📋 Task Completion Status

| Task | Status | Deliverables |
|:---|:---:|:---|
| **Task 1: Foundation** | ✅ Complete | EDA notebook, events database, workflow document |
| **Task 2: Modeling** | ✅ Complete | Bayesian models, 4 change points, impact quantification |
| **Task 3: Dashboard** | ✅ Complete | Flask API, React frontend, interactive visualization |

---

## 🎓 Learning Outcomes

- **Change Point Analysis**: Detecting structural breaks in time series
- **Bayesian Inference**: PyMC, MCMC sampling, convergence diagnostics
- **Statistical Modeling**: Regime-switching models, hypothesis testing
- **Full-Stack Development**: Flask backend, React frontend, REST APIs
- **Data Communication**: Interactive dashboards for stakeholder engagement

---

## 📚 References

- PyMC Documentation: https://www.pymc.io/
- Recharts: http://recharts.org/
- 10 Academy Curriculum: Week 11 - Change Point Analysis

---

## 🤝 Contributing

This is an educational project for 10 Academy's AI Mastery program. For questions:
- Slack: `#all-week11`
- Office Hours: Mon-Fri, 08:00-15:00 UTC

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Habtamu Wendifraw**  
10 Academy - Artificial Intelligence Mastery  
February 2026

---

**Repository**: (https://github.com/Habtu32/brent_oil_change_point_analysis)  
**Live Demo**:   
**Documentation**:

---

*This project demonstrates end-to-end data science workflow: from raw data to interactive deployment, with rigorous statistical methodology and professional software engineering practices.*
```
