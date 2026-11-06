from fastapi import FastAPI, HTTPException
from .models import ForecastRequest, ForecastResponse
from .core import DemandModel

app = FastAPI()
model = DemandModel()

@app.post("/predict", response_model=ForecastResponse)
async def predict(req: ForecastRequest):
    try:
        pred = model.predict(req.historical_sales, req.promotional_events)
        return ForecastResponse(sku_id=req.sku_id, prediction=pred, confidence_interval=0.05)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))