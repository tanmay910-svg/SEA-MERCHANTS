# AI/ML

This directory contains the SEA MERCHANTS intelligence layer.

## Selected Models

| Module | Method |
|---|---|
| Freight market forecasting | Gradient Boosting Regressor |
| Port delay prediction | Linear Regression |
| High-delay risk classification | Logistic Regression |
| Risk cost | Probability × Impact |
| Vessel selection | Feasibility constraints + expected total cost minimization |
| Charter timing | Forecast + scenario cost simulation |

## Pipeline

```text
BDI → Forecast → Port Delay/Risk → Voyage Economics → Vessel Feasibility
→ Expected Total Cost → Charter Timing → Explainable Recommendation
```

## Backend Contract

The engine should return:

```json
{
  "freight_forecast": {},
  "port_risk": {},
  "vessel_recommendation": {},
  "vessel_ranking": [],
  "explanation": "..."
}
```

Large datasets, model artifacts and secrets should not be committed unless the team explicitly decides they belong in Git LFS or another artifact store.
