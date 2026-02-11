```markdown
# Brent Oil Change Point Analysis

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyMC 5.8+](https://img.shields.io/badge/PyMC-5.8+-orange.svg)](https://www.pymc.io/)
[![React 18+](https://img.shields.io/badge/React-18+-61DAFB.svg?logo=react)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Bayesian Change Point Detection and Interactive Visualization of Structural Breaks in Brent Crude Oil Prices (1987–2022)**  
> 10 Academy – Week 11 Challenge | Artificial Intelligence Mastery | February 2026

---

## 🎯 Project Overview

This repository implements **Bayesian change point detection** on 35 years of daily Brent crude oil prices to identify structural breaks driven by major geopolitical events, economic crises, and OPEC policy shifts.

Using **PyMC** for probabilistic modeling, the analysis quantifies the timing, magnitude, and uncertainty of regime changes in both price levels and volatility. An interactive **React** dashboard enables exploration of results, posterior distributions, and event annotations.

The insights support:
- Investment timing and risk management
- Policy impact assessment
- Hedging strategies for energy market participants

### Business Problem

Birhan Energies, a leading energy consultancy, seeks data-driven evidence of how exogenous shocks affect oil price dynamics. This project delivers:

| Stakeholder       | Key Question                                      | Delivered Solution                              |
|-------------------|---------------------------------------------------|-------------------------------------------------|
| **Investors**     | When do regime shifts signal buy/sell opportunities? | Precise change point dates with credible intervals |
| **Policymakers**  | Which interventions produced measurable effects?   | Event-aligned structural breaks                 |
| **Energy Firms**  | How to anticipate and hedge volatility spikes?    | Quantified shifts in volatility regimes         |

### Key Findings

| Change Point          | Approximate Date | Price Impact (Cumulative) | Volatility Multiplier | Associated Event                     |
|-----------------------|------------------|---------------------------|-----------------------|--------------------------------------|
| Gulf War              | 1990-08         | +100%                     | 3.4×                  | Iraq invades Kuwait                  |
| Global Financial Crisis | 2008-09       | -70%                      | 2.4×                  | Lehman Brothers collapse             |
| OPEC Price War        | 2014-11         | -60%                      | 2.5×                  | OPEC abandons production quotas      |
| COVID-19 Pandemic     | 2020-03         | -80% (briefly negative)   | 6.2×                  | Global demand collapse               |

> Note: Impacts are approximate regime-shift magnitudes derived from posterior distributions.

---

## 🏗️ Repository Structure

```
.
├── data/
│   └── raw/brent_daily_1987_2022.csv          # Source price data
├── notebooks/
│   ├── 01_data_exploration.ipynb             # EDA and preprocessing
│   ├── 02_bayesian_change_point_model.ipynb  # PyMC model definition & inference
│   └── 03_posterior_analysis.ipynb           # Results summarization
├── backend/
│   ├── model.py                              # Reusable PyMC model code
│   ├── inference.py                          # Sampling and posterior processing
│   └── utils.py                              # Data loading and helpers
├── frontend/
│   ├── public/                               # Static assets
│   ├── src/
│   │   ├── components/                       # Dashboard components
│   │   ├── App.jsx                           # Main application
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── results/
│   ├── traces/                               # Saved posterior traces
│   └── figures/                              # Static plots
├── requirements.txt                          # Python dependencies
├── package.json                              # Frontend dependencies
├── LICENSE
└── README.md
```

---

## 🛠️ Technologies Used

- **Python 3.9+** – Data processing and modeling
- **PyMC 5.8+** – Bayesian inference and change point modeling
- **ArviZ** – Posterior visualization and diagnostics
- **Pandas, NumPy, Matplotlib, Seaborn** – Data manipulation and static plots
- **React 18+** – Interactive dashboard
- **Recharts / Plotly.js** – Web-based visualizations
- **Vite** – Frontend build tool

---

## 🚀 Installation

### Backend (Python)

```bash
git clone https://github.com/your-username/brent-oil-change-point-analysis.git
cd brent-oil-change-point-analysis

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Frontend (React)

```bash
cd frontend
npm install
```

---

## 📊 Usage

### Run the Bayesian Model

```bash
cd backend
python inference.py        # Performs sampling and saves traces
```

Results and figures will be saved to `../results/`.

### Launch Interactive Dashboard

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` to explore:
- Time series with annotated change points
- Posterior distributions of change point locations
- Regime-specific mean and volatility estimates
- Event timeline overlay

---

## 📈 Sample Visualizations

(Include screenshots here in your actual repository)

- Posterior distribution of change point timings
- Trace plot of price regimes
- Interactive dashboard preview

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to open a pull request or issue.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgments

- 10 Academy for the challenge and training
- PyMC developers for the excellent probabilistic programming framework
- Brent crude oil price data sourced from public EIA/API repositories

---
```
