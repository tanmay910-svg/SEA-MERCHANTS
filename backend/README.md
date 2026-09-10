# Backend

Backend/API workspace for SEA MERCHANTS.

## Responsibilities

- Receive cargo/voyage scenarios
- Validate inputs
- Call the AI/ML intelligence engine
- Expose recommendation endpoints
- Handle database/persistence integrations
- Return normalized JSON to the frontend

## AI/ML Boundary

Backend should treat the AI/ML module as a decision engine. Do not duplicate model logic in the frontend.

Recommended API shape:

`POST /api/recommend`

Input: cargo quantity, origin, destination, required window, fuel type and applicable cost inputs.

Output: freight forecast, port risk, vessel ranking, recommended vessel, charter timing and explanation.
