import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

FEATURE_LAGS = [1, 2, 3, 6, 12]
ROLLING_WINDOWS = [3, 6, 12]

def make_features(history: pd.Series) -> pd.DataFrame:
    history = history.sort_index().astype(float)
    x = pd.DataFrame(index=history.index)
    for lag in FEATURE_LAGS:
        x[f"lag_{lag}"] = history.shift(lag)
    for w in ROLLING_WINDOWS:
        x[f"mean_{w}"] = history.shift(1).rolling(w).mean()
        x[f"std_{w}"] = history.shift(1).rolling(w).std()
    x["month"] = history.index.month
    x["year"] = history.index.year
    return x.dropna()

class BDIForecaster:
    """Explainable prototype BDI forecasting model."""
    def __init__(self):
        self.model = GradientBoostingRegressor(
            n_estimators=250, max_depth=2, learning_rate=0.03,
            loss="huber", random_state=42
        )

    def fit(self, bdi_df):
        d = bdi_df.copy()
        d["date"] = pd.to_datetime(d["date"])
        s = d.sort_values("date").set_index("date")["bdi"].astype(float)
        self.history = s.copy()
        f = make_features(s)
        self.model.fit(f, s.loc[f.index])
        return self

    def forecast(self, periods=6):
        h = self.history.copy()
        dates = pd.date_range(h.index[-1] + pd.offsets.MonthBegin(1), periods=periods, freq="MS")
        preds = []
        for dt in dates:
            temp = pd.concat([h, pd.Series([np.nan], index=[dt])])
            row = make_features(temp).loc[[dt]]
            pred = float(self.model.predict(row)[0])
            preds.append(pred)
            h.loc[dt] = pred
        return pd.DataFrame({"date": dates, "forecast_bdi": preds})

    @staticmethod
    def market_condition(bdi_value):
        if bdi_value < 1000: return "Low"
        if bdi_value < 2000: return "Moderate"
        if bdi_value < 3000: return "High"
        return "Very High"
