"""Port delay and high-delay risk models."""
from __future__ import annotations
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression

class PortIntelligence:
    def __init__(self, delay_threshold=None):
        self.delay_model = LinearRegression()
        self.risk_model = LogisticRegression(max_iter=1000)
        self.delay_threshold = delay_threshold
        self.feature_columns = None

    def fit(self, X, delay_hours):
        X = X.copy()
        y = np.asarray(delay_hours, dtype=float)
        self.feature_columns = list(X.columns)
        self.delay_model.fit(X, y)
        threshold = self.delay_threshold
        if threshold is None:
            threshold = float(np.quantile(y, 0.75))
        self.delay_threshold = threshold
        self.risk_model.fit(X, (y >= threshold).astype(int))
        return self

    def predict(self, X):
        X = X[self.feature_columns]
        delay = np.maximum(0, self.delay_model.predict(X))
        risk = self.risk_model.predict_proba(X)[:, 1]
        return delay, risk
