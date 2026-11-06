from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post("/predict", json={
        "sku_id": "test-1",
        "historical_sales": [10, 20, 30],
        "promotional_events": [0, 1, 0]
    })
    assert response.status_code == 200
    assert "prediction" in response.json()