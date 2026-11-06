# Demand Forecaster

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-ready machine learning service that predicts future product demand and inventory requirements based on historical transaction logs and promotional events. **Demand Forecaster** trains regression models on temporal telemetry, evaluates metric accuracy, and serves high-throughput prediction endpoints for inventory planning pipelines.

---

## Problem Statement & Target Audience

### The Problem
Retailers and e-commerce platforms frequently suffer from severe revenue loss due to **stockouts** or bloated holding costs caused by **overstocking**. Traditional inventory planning relies on manual estimation or naive extrapolation (e.g., simple moving averages), which consistently fail to capture:
- Complex day-of-week and seasonal patterns.
- Uplift spikes driven by marketing promotions and discount events.
- Non-linear temporal dependencies across multiple SKUs.

Enterprise forecasting solutions are often cost-prohibitive, closed-source, or difficult to cleanly embed into custom backend ordering and supply-chain systems.

### Target Audience
- **Backend Engineers & MLOps Teams** looking for a lightweight, embeddable microservice for automated replenishment calculations.
- **E-Commerce & Supply Chain Platforms** needing an open, extensible Python service for SKU-level demand forecasting.
- **Data Scientists** requiring a structured baseline architecture for temporal feature engineering and regression model serving.

---

## Key Features

- **Advanced Feature Engineering Pipeline**: Extracts temporal attributes including seasonality, day-of-week trends, lag variables, rolling averages, and promotional indicators from raw transaction logs.
- **Flexible Model Training & Artifact Management**: Train and cross-validate multiple Scikit-Learn regression algorithms (e.g., Random Forest, Ridge, Gradient Boosting) with automated serialization using `Joblib`.
- **High-Performance RESTful API**: Built with FastAPI and validated via Pydantic for retrieving single-SKU predictions, high-volume batch forecasts, and real-time model evaluation metrics.
- **Diagnostic Visualization Suite**: Integrated Matplotlib utilities for automated generation of demand trend curves and residual distribution charts for model inspection and reporting.

---

## Architecture & System Design

```
                     +----------------------------------+
                     |   Client Application / Pipeline  |
                     +----------------------------------+
                                      |
                                  HTTP / REST
                                      |
                                      v
                     +----------------------------------+
                     |     FastAPI Server (src/main.py) |
                     +----------------------------------+
                                      |
                         Route Processing (src/api.py)
                                      |
             +------------------------+------------------------+
             |                                                 |
             v                                                 v
+-------------------------+                       +-------------------------+
| Feature Engineering     |                       | Core Engine             |
| (src/preprocessing.py)  |                       | (src/core.py)           |
|  - Seasonality & Lags   |                       |  - Model Training       |
|  - Rolling Statistics   |                       |  - Metric Evaluation    |
|  - Promo Indicators     |                       |  - Joblib Serialization |
+-------------------------+                       +-------------------------+
             |                                                 |
             +------------------------+------------------------+
                                      |
                                      v
                     +----------------------------------+
                     |  Visualization (src/visualization) |
                     |  - Trend Plots & Residual Analysis|
                     +----------------------------------+
```

### Module Breakdown

| Module | Purpose |
| :--- | :--- |
| **`src/models.py`** | Pydantic domain schemas for request validation, feature payload structure, and API response typing. |
| **`src/preprocessing.py`** | Feature engineering logic for building seasonality, rolling averages, lag features, and promotional indicators. |
| **`src/core.py`** | Orchestration of model training, hyperparameter cross-validation, evaluation metrics, inference pipelines, and Joblib artifact management. |
| **`src/visualization.py`** | Matplotlib utilities for generating diagnostic charts, residual analysis plots, and forecast vs. actual trend visualizations. |
| **`src/api.py`** | FastAPI endpoints handling single-SKU forecasting, batch predictions, model retraining triggers, and metrics reporting. |
| **`src/main.py`** | Application entry point executing ASGI Uvicorn server initialization and lifespan events. |

---

## Technology Stack

| Category | Technology | Usage |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core language execution environment |
| **Web Framework** | FastAPI | Async REST API service definition |
| **Data Validation** | Pydantic | Schema definitions and payload validation |
| **Data Processing** | Pandas | Tabular data manipulation and temporal calculations |
| **Machine Learning**| Scikit-Learn | Regression algorithms, metrics, and cross-validation |
| **Model Persistence**| Joblib | Model binary artifact serialization and loading |
| **Visualization** | Matplotlib | Programmatic trend graph and residual plot rendering |
| **Testing** | pytest | Automated unit and integration testing suite |

---

## Installation & Virtual Environment Setup

### Prerequisites
- Python `3.10` or higher installed.
- `pip` package manager.

### Step-by-Step Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-organization/demand-forecaster.git
   cd demand-forecaster
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Environment Variables Configuration

The application uses environment variables for operational configuration. Copy the example configuration to create your local `.env` file:

```bash
cp .env.example .env
```

### Supported Variables (`.env`)

```ini
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Artifact Path Configuration
MODEL_DIR=artifacts/models
PLOT_OUTPUT_DIR=artifacts/plots

# Forecasting Parameters
DEFAULT_MODEL_TYPE=RandomForest
CROSS_VALIDATION_FOLDS=5
```

---

## Usage Guide

### 1. Running the API Server

Start the production-ready Uvicorn server:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Once running, interactive OpenAPI (Swagger) documentation is available at `http://localhost:8000/docs`.

---

### 2. Primary REST API Endpoints

#### `POST /api/v1/predict`
Request a single SKU demand forecast.

*Request:*
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/predict' \
  -H 'Content-Type: application/json' \
  -d '{
    "sku_id": "SKU-9842",
    "timestamp": "2026-04-01T00:00:00Z",
    "is_promotion": true,
    "historical_sales_7d_avg": 142.5,
    "historical_sales_30d_avg": 118.2
  }'
```

*Response:*
```json
{
  "sku_id": "SKU-9842",
  "forecast_date": "2026-04-01T00:00:00Z",
  "predicted_demand": 168.4,
  "confidence_interval": {
    "lower_bound": 155.1,
    "upper_bound": 181.7
  },
  "model_version": "v1.2.0"
}
```

---

#### `POST /api/v1/predict/batch`
Request batch forecasts for multiple historical telemetry rows.

*Request:*
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/predict/batch' \
  -H 'Content-Type: application/json' \
  -d '{
    "records": [
      {
        "sku_id": "SKU-1001",
        "timestamp": "2026-04-01T00:00:00Z",
        "is_promotion": false,
        "historical_sales_7d_avg": 45.0,
        "historical_sales_30d_avg": 42.1
      },
      {
        "sku_id": "SKU-1002",
        "timestamp": "2026-04-01T00:00:00Z",
        "is_promotion": true,
        "historical_sales_7d_avg": 89.0,
        "historical_sales_30d_avg": 70.3
      }
    ]
  }'
```

---

#### `GET /api/v1/metrics`
Retrieve accuracy scores for the active model artifacts.

*Request:*
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/metrics'
```

*Response:*
```json
{
  "active_model": "RandomForestRegressor",
  "metrics": {
    "rmse": 12.45,
    "mae": 8.32,
    "r2_score": 0.914,
    "mape": 0.065
  },
  "last_trained": "2026-03-15T14:22:00Z"
}
```

---

## Automated Testing Instructions

The project uses `pytest` for unit tests across core algorithms, API endpoints, and feature engineering procedures.

### Execute All Unit Tests

```bash
pytest
```

### Execute Tests with Detailed Verbosity and Coverage

```bash
pytest -v --cov=src --cov-report=term-missing
```

### Execute Specific Test Modules

```bash
# Preprocessing tests
pytest tests/test_preprocessing.py

# Core inference and training tests
pytest tests/test_core.py

# FastAPI route endpoint tests
pytest tests/test_api.py
```

---

## Project Structure

```
demand-forecaster/
├── .env.example
├── .gitignore
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── api.py
│   ├── core.py
│   ├── main.py
│   ├── models.py
│   ├── preprocessing.py
│   └── visualization.py
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_core.py
    └── test_preprocessing.py
```

---

## Roadmap & Future Enhancements

- [ ] **Advanced Deep Learning Models**: Integrate PyTorch-based temporal networks (Temporal Fusion Transformer, N-BEATS) for non-linear long-horizon forecasting.
- [ ] **External Variable Ingestion**: Add features for weather data, macro-economic indices, and competitor pricing signals.
- [ ] **Real-Time Stream Processing**: Kafka consumer integration to continuously compute rolling statistics on incoming point-of-sale stream events.
- [ ] **Automated Retraining Pipelines**: Trigger model retraining automatically on data drift detection via MLflow integration.

---

## License

Distributed under the **MIT License**. See `LICENSE` for details.