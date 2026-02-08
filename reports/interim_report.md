# Brent Oil Change Point Analysis: Task 1 Foundation

## Executive Summary
Analysis of 9,011 daily Brent oil price observations (May 20, 1987 - September 30, 2022) to identify structural breaks using Bayesian change point detection. Data exhibits five distinct price regimes with the most significant structural break occurring during the 2014-2016 shale revolution/OPEC price war.

## 1. Data Analysis Workflow

### Phase 1: Foundation (Completed)
1. **Data Acquisition**: Loaded 9,011 daily observations from 1987-2022
2. **Quality Assurance**: Zero missing values, zero duplicates, full date coverage
3. **Feature Engineering**: Created 27 features including log returns, volatility measures, and time components
4. **Exploratory Analysis**: Identified five distinct price regimes through visual inspection

### Phase 2: Statistical Modeling (Planned)
1. **Bayesian Change Point Detection**: Implement PyMC model with discrete uniform prior for change points
2. **MCMC Sampling**: 4 chains, 2000 samples, convergence verification (R-hat ≈ 1.0)
3. **Event Association**: Match detected change points to researched geopolitical events
4. **Impact Quantification**: Calculate posterior distributions of before/after price levels

### Phase 3: Communication (Planned)
1. **Interactive Dashboard**: Flask/React application for stakeholder exploration
2. **Technical Report**: Blog-style documentation of methodology and findings
3. **Presentation**: Summary for non-technical stakeholders

## 2. Time Series Properties

| Property | Finding | Implication for Modeling |
|----------|---------|------------------------|
| **Trend** | Multi-regime non-stationary | Use log returns for stationarity |
| **Stationarity** | ADF = -12.60, p &lt; 0.001 | Returns suitable for change point detection |
| **Volatility** | Clustering around crises | Model may need variance change points |
| **Regimes** | 5 visually distinct eras | Expect 4-6 change points |

### Visual Regime Identification
1. **1987-2000**: Stable low ($10-25) - "Cheap Oil Era"
2. **2000-2008**: Steady climb to peak ($25-143) - "China Boom"
3. **2008-2009**: Financial crisis crash ($143-40) - "Great Recession"
4. **2009-2014**: High plateau ($80-120) - "$100 Era"
5. **2014-2016**: Structural break ($115-30) - "Shale Revolution" ⭐
6. **2016-2022**: Volatile recovery ($30-130) - "New Normal"

## 3. Change Point Model Design

### Model Specification
- **Likelihood**: Normal distribution with regime-specific mean and variance
- **Change Points**: Discrete uniform prior over time index
- **Sampling**: NUTS sampler via PyMC
- **Validation**: Gelman-Rubin statistic (R-hat), effective sample size, trace plots

### Expected Outputs
1. **Posterior distribution of τ (tau)**: Probability of change at each date
2. **Regime parameters**: μ₁, μ₂, σ₁, σ₂ with credible intervals
3. **Impact magnitude**: Percentage change between regimes
4. **Uncertainty quantification**: 95% credible intervals for all estimates

## 4. Event Database

Compiled 14 major events across three categories:

| Category | Count | Examples |
|----------|-------|----------|
| Conflict | 5 | Gulf War, Iraq War, Libya, Saudi attack, Ukraine |
| Economic | 3 | Asian Crisis, 2008 Financial Crisis, COVID-19 |
| Policy | 6 | OPEC decisions, EU sanctions |

**Primary Change Point Candidate**: November 27, 2014 (OPEC no-cut decision) coinciding with the visible price collapse from $115 to $30.

## 5. Critical Assumptions & Limitations

### Assumptions
1. **Discrete changes**: Market shifts occur at specific points rather than gradually
2. **Regime stability**: Statistical properties remain constant within regimes
3. **Event relevance**: Major geopolitical events drive detectable structural breaks
4. **Data quality**: Historical prices accurately reflect market conditions without systematic bias

### Limitations

#### Correlation vs. Causation
&gt; **Critical Distinction**: Statistical models identify WHEN changes occurred. Associating these with specific events requires domain expertise and represents temporal correlation, not proven causation.

**Example**: A change point detected in November 2014 correlates with the OPEC no-cut decision. However:
- Markets may have anticipated the decision (change before announcement)
- Concurrent factors (US shale production data) may have driven the shift
- The model demonstrates **temporal association**, not **causal proof**

**Mitigation Strategies**:
- Cross-reference multiple independent sources
- Analyze event windows (±30 days) for clustering
- Consider alternative explanations in interpretation
- Explicitly state uncertainty in all communications

### Model Limitations
- **Single change point model** may miss rapid successive shifts
- **Normal likelihood** assumes symmetric returns (oil has fat tails)
- **Known events bias**: Focus on researched events may miss unknown drivers

## 6. Communication Strategy

| Stakeholder | Primary Channel | Format | Key Message |
|-------------|----------------|--------|-------------|
| Investment Analysts | Interactive Dashboard | Visual + metrics | "Buy/sell signals with confidence intervals" |
| Energy Policymakers | PDF Report + Briefing | Narrative + policy implications | "Which interventions had measurable market impact" |
| Risk Managers | API + Dashboard | Real-time metrics | "Hedge timing and exposure limits" |
| Technical Audiences | GitHub + Blog Post | Code + methodology | "Reproducible Bayesian approach" |

## 7. Deliverables Status

| Deliverable | Status | Location |
|-------------|--------|----------|
| Data pipeline | ✅ Complete | `src/data/` |
| EDA notebook | ✅ Complete | `notebooks/01_eda.ipynb` |
| Processed data | ✅ Complete | `data/processed/features_engineered.csv` |
| Event database | ✅ Complete | `data/external/geopolitical_events.csv` |
| This workflow document | ✅ Complete | `reports/interim_report.md` |

## 8. Next Steps (Task 2)

1. **Implement Bayesian model** in PyMC with single change point
2. **Verify MCMC convergence** using diagnostic statistics
3. **Extend to multiple change points** for comprehensive analysis
4. **Quantify impacts** with posterior distributions
5. **Associate with events** using researched database

---

**Prepared for**: 10 Academy - Week 11 Challenge  
**Date**: February 2026  
**Data Period**: May 20, 1987 - September 30, 2022 (9,011 observations)  
**Analyst**: Habtamu Wendifraw