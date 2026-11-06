import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.utils.validation import check_is_fitted
from .preprocessing import engineer_features

class DemandModel:
    def __init__(self, path: str = "models/demand_model.joblib"):
        self.path = path
        if os.path.exists(self.path):
            try:
                self.model = joblib.load(self.path)
            except Exception:
                self.model = RandomForestRegressor()
        else:
            self.model = RandomForestRegressor()

    def train(self, X, y):
        self.model.fit(X, y)
        dirname = os.path.dirname(self.path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        joblib.dump(self.model, self.path)

    def predict(self, sales, promos):
        df = engineer_features(sales, promos)
        try:
            check_is_fitted(self.model)
        except Exception:
            self.train(df, df['sales'])
        return float(self.model.predict(df.tail(1))[0])

    def get_metrics(self, X_test, y_test):
        preds = self.model.predict(X_test)
        return {"mse": mean_squared_error(y_test, preds), "r2_score": r2_score(y_test, preds)}