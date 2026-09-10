"""BDI freight-market forecasting model for SEA MERCHANTS."""
from __future__ import annotations
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

LAGS = (1, 2, 3, 6, 12)
ROLLS = (3, 6, 12)

def make_features(series: pd.Series) -> pd.DataFrame:
    s = pd.Series(series, dtype="float64").copy()
    df = pd.DataFrame({"bdi": s})
    for lag in LAGS:
        df[f"lag_{lag}"] = s.shift(lag)
    for w in ROLLS:
        df[f"roll_mean_{w}"] = s.shift(1).rolling(w).mean()
        df[f"roll_std_{w}"] = s.shift(1).rolling(w).std()
    df["month"] = df.index.month if isinstance(df.index, pd.DatetimeIndex) else range(len(df))
    return df.dropna()

class BDIForecaster:
    def __init__(self, **kwargs):
        self.model = GradientBoostingRegressor(random_state=42, **kwargs)
        self.features = None
        self.history = None

    def fit(self, series: pd.Series):
        s = pd.Series(series, dtype="float64").dropna().sort_index()
        data = make_features(s)
        self.features = [c for c in data.columns if c != "bdi"]
        self.model.fit(data[self.features], data["bdi"])
        self.history = s.copy()
        return self

    def forecast(self, periods: int = 6) -> pd.Series:
        if self.history is None:
            raise RuntimeError("Fit the forecaster before forecasting.")
        history = self.history.copy()
        out = []
        for _ in range(periods):
            idx = history.index[-1] + pd.offsets.MonthBegin(1)
            row = {f"lag_{l}": history.iloc[-l] for l in LAGS}
            for w in ROLLS:
                vals = history.iloc[-w:]
                row[f"roll_mean_{w}"] = vals.mean()
                row[f"roll_std_{w}"] = vals.std()
            row["month"] = idx.month
            pred = float(self.model.predict(pd.DataFrame([row])[self.features])[0])
            history.loc[idx] = pred
            out.append((idx, pred))
        return pd.Series(dict(out), name="forecast_bdi")
