from pydantic import BaseModel, Field
from typing import List, Optional

class ForecastRequest(BaseModel):
    sku_id: str
    historical_sales: List[float]
    promotional_events: List[int]

class ForecastResponse(BaseModel):
    sku_id: str
    prediction: float
    confidence_interval: float

class ModelMetrics(BaseModel):
    mse: float
    r2_score: float