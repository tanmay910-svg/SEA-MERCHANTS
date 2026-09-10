from models.bdi_model import BDIForecaster
from models.port_model import PortIntelligence
from engine.economics import rank_vessels

class SeaMerchantsEngine:
    """Coordinates ML predictions with voyage economics and vessel selection."""
    def __init__(self, bdi_df, port_dwell_df):
        self.bdi = BDIForecaster().fit(bdi_df)
        self.port = PortIntelligence().fit(port_dwell_df)

    def forecast_market(self, periods=6):
        fc = self.bdi.forecast(periods)
        fc["market_condition"] = fc["forecast_bdi"].apply(self.bdi.market_condition)
        return fc

    def port_prediction(self, port_name, date):
        return self.port.predict(port_name, date)

    def vessel_recommendation(self, vessels, ports, routes, cargo_tonnes, origin,
                              destination, fuel_price, freight_rate, port_cost,
                              other_cost, expected_risk_cost, expected_port_days):
        ranking = rank_vessels(vessels, ports, routes, fuel_price, freight_rate,
                               cargo_tonnes, origin, destination, port_cost,
                               other_cost, expected_risk_cost, expected_port_days)
        if ranking.empty:
            raise ValueError("No feasible vessel satisfies the cargo and draft constraints.")
        best = ranking.iloc[0].to_dict()
        return {"recommended_vessel": best, "ranking": ranking.to_dict("records"),
                "explanation": (f"Recommended {best['Vessel_ID']} because it has the lowest "
                                "expected total voyage cost among feasible vessels.")}
