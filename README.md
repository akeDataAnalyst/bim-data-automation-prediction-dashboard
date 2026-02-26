# BIM Data Automation & Prediction Dashboard

Automated IFC-like data extraction, validation, clash simulation, anomaly detection, quantity takeoff and predictive analytics for construction & interiors projects.


## Features

- Automated data quality report (missing fields, duplicates, date logic)  
- Simulated clash detection (rule-based on room + type + count)  
- Anomaly detection on quantities & costs (Isolation Forest)  
- Prediction of missing quantities (Area_m2, Volume_m3) & total costs  
- Streamlit dashboard with:
  - Sidebar filters (element type, material, cost range)  
  - Metrics (total elements, predicted costs, anomalies, clashes)  
  - Cost distribution histogram  
  - Predicted vs actual cost scatter  
  - Interactive table with CSV download  
  - Anomalies & clashes summary

## Tech Stack

| Layer                 | Tools / Libraries                              |
|-----------------------|------------------------------------------------|
| Language              | Python 3.10+                                   |
| Data Processing       | pandas, numpy                                  |
| ML / Prediction       | scikit-learn (RandomForestRegressor, IsolationForest) |
| Dashboard             | Streamlit, Plotly                              |
| File Handling         | pathlib                                        |


## Results & Performance
- Dataset: 950 synthetic BIM elements (2020–2025 dates)  
- Quality checks: No duplicates, 15% missing geometric data, 47% date logic issues  
- Clash simulation: 19% potential clashes  
- Anomaly detection: 8% cost/quantity anomalies  
- Prediction MAE (on known data):Area_m2: 5.23 m²  
- Volume_m3: 2.24 m³  
- TotalCost_ETB: 43,435 ETB
