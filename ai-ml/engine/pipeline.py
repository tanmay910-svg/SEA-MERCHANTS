"""High-level recommendation helpers."""
from .economics import rank_vessels

def recommend_vessel(vessels, cargo_tonnes, max_draft=None):
    ranked = rank_vessels(vessels, cargo_tonnes, max_draft)
    if not ranked:
        return None, []
    return ranked[0], ranked

def explain_recommendation(vessel):
    if vessel is None:
        return "No feasible vessel satisfies the supplied constraints."
    return (f"Recommended {vessel.get('name', 'vessel')} because it has the lowest "
            "expected total voyage cost among vessels satisfying the cargo-capacity "
            "and port constraints.")
