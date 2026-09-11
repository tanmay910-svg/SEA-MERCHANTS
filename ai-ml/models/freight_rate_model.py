"""SEA MERCHANTS freight-rate prediction model loader.

The trained artifact is expected at ai-ml/models/best_freight_rate_model.joblib.
The artifact contains the preprocessing pipeline and trained Random Forest.
"""
from pathlib import Path
import pandas as pd
import joblib

MODEL_PATH = Path(__file__).resolve().parent / "best_freight_rate_model.joblib"


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Trained model not found at {MODEL_PATH}. "
            "Copy best_freight_rate_model.joblib into ai-ml/models/."
        )
    return joblib.load(MODEL_PATH)


def predict_freight_rate(payload: dict) -> float:
    """Predict freight rate in USD/tonne from one shipment payload."""
    model = load_model()
    frame = pd.DataFrame([payload])
    return float(model.predict(frame)[0])
