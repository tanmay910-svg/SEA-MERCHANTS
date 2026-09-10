"""Transparent voyage economics and vessel ranking."""
from __future__ import annotations

def voyage_days(distance_nm, speed_knots, port_days=0, expected_delay_days=0):
    return distance_nm / (speed_knots * 24.0) + port_days + expected_delay_days

def fuel_cost(daily_fuel_tonnes, days, fuel_price_per_tonne):
    return daily_fuel_tonnes * days * fuel_price_per_tonne

def landed_cost(cargo_cost, freight_cost, port_handling_cost, other_logistics_cost):
    return cargo_cost + freight_cost + port_handling_cost + other_logistics_cost

def expected_risk_cost(risks):
    return sum(float(r.get("probability", 0)) * float(r.get("impact", 0)) for r in risks)

def expected_total_cost(cargo_cost, freight_cost, port_handling_cost, other_logistics_cost, risk_cost=0):
    return landed_cost(cargo_cost, freight_cost, port_handling_cost, other_logistics_cost) + risk_cost

def rank_vessels(vessels, cargo_tonnes, max_draft=None):
    feasible = []
    for v in vessels:
        if v.get("capacity_tonnes", 0) < cargo_tonnes:
            continue
        if max_draft is not None and v.get("draft_m", 999) > max_draft:
            continue
        feasible.append(v)
    return sorted(feasible, key=lambda x: x["expected_total_cost"])
