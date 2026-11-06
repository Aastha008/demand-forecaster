from src.core import DemandModel
import numpy as np

def test_model_training():
    model = DemandModel(path="test_model.joblib")
    X = np.random.rand(10, 3)
    y = np.random.rand(10)
    model.train(X, y)
    assert model.model is not None