def voyage_costs(cargo_tonnes, vessel_row, route_row, fuel_price, freight_rate,
                 port_cost, other_cost, expected_risk_cost, expected_port_days):
    voyage_days = route_row.Distance_nm / (vessel_row.Speed_knots * 24) + expected_port_days
    fuel_used = vessel_row.Fuel_Consumption_tpd * voyage_days
    freight_cost = cargo_tonnes * freight_rate
    fuel_cost = fuel_used * fuel_price
    total = freight_cost + fuel_cost + port_cost + other_cost + expected_risk_cost
    return {
        "Voyage_Days": float(voyage_days),
        "Fuel_Used_tonnes": float(fuel_used),
        "Freight_Cost_USD": float(freight_cost),
        "Fuel_Cost_USD": float(fuel_cost),
        "Port_Cost_USD": float(port_cost),
        "Other_Cost_USD": float(other_cost),
        "Expected_Risk_Cost_USD": float(expected_risk_cost),
        "Expected_Total_Cost_USD": float(total),
    }

def rank_vessels(vessels, ports, routes, fuel_price, freight_rate,
                 cargo_tonnes, origin, destination, port_cost, other_cost,
                 expected_risk_cost, expected_port_days):
    route = routes[(routes.Origin_Port == origin) &
                   (routes.Destination_Port == destination)].iloc[0]
    max_draft = min(float(ports.loc[ports.Port == origin, "Max_Draft_m"].iloc[0]),
                    float(ports.loc[ports.Port == destination, "Max_Draft_m"].iloc[0]))
    feasible = vessels[(vessels.DWT_tonnes >= cargo_tonnes) &
                       (vessels.Draft_m <= max_draft)].copy()
    rows = []
    for _, v in feasible.iterrows():
        costs = voyage_costs(cargo_tonnes, v, route, fuel_price, freight_rate,
                             port_cost, other_cost, expected_risk_cost, expected_port_days)
        rows.append({"Vessel_ID": v.Vessel_ID, "Vessel_Type": v.Vessel_Type,
                     "DWT_tonnes": v.DWT_tonnes, "Draft_m": v.Draft_m,
                     "Speed_knots": v.Speed_knots, **costs})
    import pandas as pd
    return pd.DataFrame(rows).sort_values("Expected_Total_Cost_USD").reset_index(drop=True)
