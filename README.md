# 🚢 SEA MERCHANTS

Smart India Hackathon prototype for explainable, data-driven maritime chartering decision support.

## Project Goal

SEA MERCHANTS helps a shipping/steel-industry decision maker evaluate a cargo voyage by combining freight-market forecasting, port intelligence, voyage economics, vessel feasibility, risk analysis, and charter-timing analysis.

**Decision support only:** the final chartering decision remains with a human user.

## System Flow

```text
Cargo / Voyage Requirements
            ↓
     Freight Forecast
            ↓
       Port Risk
            ↓
    Voyage Economics
            ↓
   Vessel Feasibility
            ↓
 Expected Total Cost
            ↓
   Charter Timing
            ↓
    Recommendation
            ↓
      Human Decision
```

## Repository Structure

```text
SEA-MERCHANTS/
├── frontend/                 # Frontend/dashboard implementation
├── backend/                  # API, services, database integration
├── ai-ml/                    # AI/ML and decision-engine implementation
│   ├── models/               # Forecasting and port models
│   ├── engine/               # Economics, risk and recommendation logic
│   ├── notebooks/            # Experiments / EDA
│   └── data/                 # Local data instructions only; large data stays out of Git
├── docs/                     # Research, architecture, SIH and technical documents
├── tests/                    # Cross-module and integration tests
├── data/                     # Shared-data instructions / metadata
├── .github/                  # GitHub workflows and templates
├── .gitignore
├── README.md
└── requirements.txt
```

## Team Responsibilities

| Area | Owner | Scope |
|---|---|---|
| AI/ML | AI/ML team | Forecasting, port risk, cost/risk intelligence, recommendation logic |
| Backend | Backend team | API, persistence, integration |
| Frontend | Frontend team | Dashboard, user inputs, visualizations |
| Integration | Integration team | Connect frontend ↔ backend ↔ AI/ML |
| Documentation | Team | SIH research, architecture, demo material |

## Current AI/ML Architecture

### Freight Market
- Candidate models evaluated: Naive, Seasonal Naive, SARIMA, Random Forest, Gradient Boosting.
- **Selected model: Gradient Boosting Regressor** based on the final walk-forward RMSE comparison.

### Port Intelligence
- **Selected delay model: Linear Regression** for expected dwell/delay hours.
- **Selected risk classifier: Logistic Regression** for high-delay probability.

### Risk

```text
Expected Risk Cost = Probability × Impact
```

For multiple risks:

```text
Expected Risk Cost = Σ(Pᵢ × Iᵢ)
```

### Vessel Selection

Hard constraints are applied first (e.g. capacity and draft compatibility), then:

```text
V* = arg min ExpectedTotalCost_v
```

### Charter Timing

Candidate charter windows are compared using forecast-driven expected total voyage cost:

```text
T* = arg min ExpectedTotalCost(t)
```

## Data Policy

SEA MERCHANTS contains both collected/public-style data and prototype synthetic/demo data.

- Real/collected data is labelled as such.
- Synthetic/prototype assumptions must be clearly labelled.
- Synthetic values must not be presented as historical real-world observations.
- Missing inputs may be supplied by the user or represented as explicit prototype assumptions.

## Getting Started

### Frontend
See `frontend/README.md` once frontend work is added.

### Backend
See `backend/README.md` once backend work is added.

### AI/ML
See `ai-ml/README.md` for the model pipeline and handoff contract.

## Contribution Workflow

1. Create a feature branch from `main`.
2. Work only inside the module you own unless integration is required.
3. Open a pull request for review.
4. Keep commits focused and descriptive.
5. Do not commit secrets, local virtual environments, or large raw datasets.
