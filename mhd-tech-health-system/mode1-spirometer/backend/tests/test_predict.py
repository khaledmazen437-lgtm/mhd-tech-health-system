"""
Basic smoke test for /predict. Requires mhd_spirometry_model.pth and
mhd_scaler.pkl to exist in ml-pipeline/artifacts before running.

Run with: pytest tests/
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_predict_valid_input():
    payload = {
        "gender": 1,
        "age_years": 55,
        "height_cm": 175,
        "weight_kg": 80,
        "fvc": 3800,
        "fev1": 2400,
        "pef": 6200,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["diagnosis"] in (0, 1)
    assert 0.0 <= body["confidence"] <= 1.0

def test_predict_rejects_invalid_age():
    payload = {
        "gender": 1,
        "age_years": -5,
        "height_cm": 175,
        "weight_kg": 80,
        "fvc": 3800,
        "fev1": 2400,
        "pef": 6200,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
