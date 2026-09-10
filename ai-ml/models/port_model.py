import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class PortIntelligence:
    """Port dwell prediction and high-delay risk classification."""
    def fit(self, port_df):
        d = port_df.copy()
        d["date"] = pd.to_datetime(d["date"])
        d["month"] = d.date.dt.month
        d["year"] = d.date.dt.year
        d["quarter"] = d.date.dt.quarter
        self.threshold = d.dwell_time_hours.quantile(0.75)
        self.pre = ColumnTransformer([
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["port_name"]),
            ("num", "passthrough", ["month", "year", "quarter"])
        ])
        self.delay_model = Pipeline([("pre", self.pre), ("model", LinearRegression())])
        self.risk_model = Pipeline([
            ("pre", self.pre),
            ("model", LogisticRegression(max_iter=2000, class_weight="balanced"))
        ])
        X = d[["port_name", "month", "year", "quarter"]]
        y = d["dwell_time_hours"]
        self.delay_model.fit(X, y)
        self.risk_model.fit(X, (y >= self.threshold).astype(int))
        return self

    def predict(self, port_name, date):
        dt = pd.Timestamp(date)
        X = pd.DataFrame([{"port_name": port_name, "month": dt.month,
                           "year": dt.year, "quarter": dt.quarter}])
        return {
            "expected_dwell_hours": max(0.0, float(self.delay_model.predict(X)[0])),
            "high_delay_probability": float(self.risk_model.predict_proba(X)[0, 1]),
            "high_delay_threshold_hours": float(self.threshold),
        }
