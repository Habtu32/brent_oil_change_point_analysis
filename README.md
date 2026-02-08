```markdown
# Brent Oil Change Point Analysis

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyMC](https://img.shields.io/badge/PyMC-5.8+-orange.svg)](https://www.pymc.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)[web:7][web:10]

> **Detecting structural breaks in Brent oil prices using Bayesian change point analysis**
>
> 10 Academy - Week 11 Challenge | February 2026[web:1][web:4]

---

## 📊 Project Overview

This project analyzes 35 years of Brent crude oil prices (1987-2022) to identify **structural breaks** (change points) caused by major geopolitical events, economic shocks, and OPEC policy decisions.[web:2][web:5] Using **Bayesian inference** and **PyMC**, we quantify the timing and magnitude of regime changes to support investment strategies, policy development, and risk management.[web:3][web:6]

### Key Question

> *"When did the oil market fundamentally change, and which events drove those changes?"*[web:8]

### Business Impact

| Stakeholder       | Application                                        |
|-------------------|----------------------------------------------------|
| **Investors**     | Timing entry/exit based on regime detection        |
| **Policymakers**  | Evaluating impact of sanctions and agreements      |
| **Energy Companies** | Hedging strategies and operational planning   |[web:2][web:5]

---

## 🗂️ Repository Structure

```text
brent-oil-change-point-analysis/
│
├── data/                          # All data files
│   ├── raw/                       # Original Brent prices (1987-2022)
│   ├── processed/                 # Cleaned data with engineered features
│   └── external/                  # Researched geopolitical events
│
├── notebooks/                     # Analysis notebooks
│   ├── 01_eda.ipynb               # Exploratory data analysis ✅
│   ├── 02_bayesian_modeling.ipynb # PyMC change point models (Phase 2)
│   └── 03_advanced_analysis.ipynb # Multiple change points (Phase 2+)
│
├── src/                           # Production code
│   ├── data/                      # Data loading & processing
│   ├── models/                    # Bayesian models
│   ├── visualization/             # Plotting utilities
│   └── dashboard/                 # Flask backend (Phase 3)
│
├── reports/                       # Documentation & outputs
│   ├── interim_report.md          # Task 1 deliverable ✅
│   └── figures/                   # Generated visualizations
│
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── .gitignore                     # Git exclusions
```[web:1][web:4]

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/brent-oil-change-point-analysis.git
cd brent-oil-change-point-analysis

# Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run EDA Notebook

```bash
cd notebooks
jupyter notebook 01_eda.ipynb
```

Execute all cells to reproduce Task 1 results:[web:1]

- Data loading (9,011 observations)[web:5]
- Feature engineering (27 features)[web:3]
- Stationarity testing (ADF: -12.60, p < 0.001)[web:5]
- Visualization of 5 distinct price regimes[web:2][web:4]

### 3. Verify Task 1 Deliverables

```bash
# Check files exist
ls data/processed/features_engineered.csv
ls data/external/geopolitical_events.csv
ls reports/interim_report.md
```

---

## 📈 Key Findings (Task 1)

### Data Summary

| Metric            | Value                                   |
|-------------------|-----------------------------------------|
| Period            | May 20, 1987 - September 30, 2022       |
| Observations      | 9,011 daily prices                      |
| Price Range       | 9.10 - 143.95 USD                       |
| Mean Price        | 46.46 USD                               |[web:5]
| Identified Regimes | See below                             |

Identified regimes:[web:2][web:4]

- 1987-2000: Stable low (10-25 USD) – "Cheap Oil Era"
- 2000-2008: Steady climb to 143 USD – "China Boom"
- 2008-2009: Financial crisis crash – "Great Recession"
- 2009-2014: High plateau (80-120 USD) – "100 USD Era"
- 2014-2016: Structural break (115 → 30 USD) – "Shale Revolution"
- 2016-2022: Volatile recovery – "New Normal"

### Statistical Validation

- ✅ Stationarity confirmed: Log returns (ADF = -12.60, p < 0.001)[web:5]
- ✅ Data quality: Zero missing values, zero duplicates[web:5]
- ✅ Features engineered: Returns, volatility, moving averages[web:3]

---

## 🛠️ Tech Stack

| Component           | Technology              |
|---------------------|------------------------|
| Language            | Python 3.9+            |
| Bayesian Modeling   | PyMC 5.8+              |
| Data Processing     | Pandas, NumPy          |
| Visualization       | Matplotlib, Seaborn, ArviZ |
| Dashboard Backend   | Flask (Phase 3)        |
| Dashboard Frontend  | React (Phase 3)        |[web:3][web:6][web:9]

---

## 📋 Task Status

| Phase            | Status        | Deliverables                         |
|------------------|--------------|--------------------------------------|
| Task 1: Foundation | ✅ COMPLETE | EDA, events database, workflow document |
| Task 2: Modeling | 🔄 IN PROGRESS | PyMC change point models            |
| Task 3: Dashboard | ⏳ PENDING  | Flask/React interactive application |[web:1][web:3]

---

## 📚 Documentation

- Task 1 Report: `reports/interim_report.md`[web:1]
- Event Database: `data/external/geopolitical_events.csv`[web:2][web:8]
- EDA Notebook: `notebooks/01_eda.ipynb`[web:4]

---

## 🤝 Contributing

This is an educational project for 10 Academy's AI Mastery program.[web:1] For questions or feedback:

- Slack: `#all-week11`
- Office Hours: Mon–Fri, 08:00–15:00 UTC[web:1]

---

## 📝 License

MIT License – See `LICENSE` for details.[web:10]
```