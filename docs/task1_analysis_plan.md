# Task 1: Analysis Plan and Foundations

## 1) Analysis workflow (data-to-insight)
1. **Data ingestion**
   - Load the Brent price series and enforce consistent datetime parsing.
   - Validate schema and identify missing or duplicated dates.
2. **Data quality checks**
   - Identify missing values, outliers, and structural breaks in coverage.
   - Document any preprocessing decisions (e.g., forward-filling vs. dropping gaps).
3. **Exploratory data analysis (EDA)**
   - Plot raw price series to observe macro trends, shocks, and volatility regimes.
   - Examine log returns for stationarity and volatility clustering.
   - Summarize basic statistics (mean, variance, rolling volatility).
4. **Baseline statistical diagnostics**
   - Conduct stationarity checks (ADF/KPSS) on price levels and returns.
   - Evaluate trend and seasonality using rolling windows and decomposition.
5. **Bayesian change point modeling**
   - Implement a single-change-point model for log returns or prices.
   - Extend to multiple change points if posterior indicates multiple breaks.
6. **Event alignment and interpretation**
   - Compare posterior change-point dates with an event table.
   - Form hypotheses about which events align with detected shifts.
7. **Insight generation & communication**
   - Quantify shifts in mean or volatility with credible intervals.
   - Prepare narrative summaries and visuals for stakeholders.

## 2) Event data compilation
A structured list of 15 high-impact events is maintained in `data/key_events.csv`. The dataset includes:
- Geopolitical conflicts (e.g., wars, supply disruptions)
- OPEC policy announcements
- Sanctions and policy responses

## 3) Assumptions and limitations
- **Correlation vs. causation:** A change point aligned with an event suggests correlation in time, not proof of causality. Additional causal inference methods or exogenous controls are required to establish causality.
- **Single-series limitation:** Brent price data alone cannot capture all macroeconomic drivers (e.g., GDP, FX, inventories).
- **Timing uncertainty:** Event impact windows can vary; single-date markers are approximations.
- **Model simplicity:** Initial change-point models assume abrupt regime shifts and may miss gradual transitions.

## 4) Communication channels and formats
- **Primary audiences:** investors, policy analysts, and energy company planners.
- **Formats:**
  - Executive summary and PDF report
  - Interactive dashboard (web-based) for exploratory analysis
  - Stakeholder slide deck for briefings

## 5) Data properties and modeling implications
- **Trend analysis:** Long-term drift and multi-year cycles suggest nonstationarity in price levels.
- **Stationarity testing:** Price levels likely nonstationary; log returns expected to be closer to stationary.
- **Volatility patterns:** Volatility clustering indicates heteroskedasticity, guiding the use of change-point or regime-switching models.

## 6) Change point model purpose (context)
Change point models identify structural breaks in a time series, helping quantify when the underlying mean or variance shifts. In the Brent price context, this supports detecting market regime shifts tied to geopolitical or policy events.

## 7) Expected outputs and limitations
- **Expected outputs:**
  - Posterior distribution of change point dates
  - Estimated pre/post parameters (mean/variance) with credible intervals
  - Model diagnostics (trace plots, R-hat, effective sample sizes)
- **Limitations:**
  - Sensitive to model specification and prior choices
  - Cannot by itself confirm causal relationships

