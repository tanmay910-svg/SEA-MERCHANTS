from engine.economics import expected_total_cost, expected_risk_cost

cargo_cost = 3_000_000
freight = 1_200_000
port = 180_000
logistics = 120_000
risks = [{"probability": 0.30, "impact": 100_000}]
risk = expected_risk_cost(risks)
total = expected_total_cost(cargo_cost, freight, port, logistics, risk)
print(f"Landed cost: ${cargo_cost + freight + port + logistics:,.0f}")
print(f"Expected risk cost: ${risk:,.0f}")
print(f"Expected total cost: ${total:,.0f}")
