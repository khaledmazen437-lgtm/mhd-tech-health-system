from fastapi import APIRouter, HTTPException

from app.schemas.patient import PatientInput, PredictionOutput
from app.services.inference_service import run_inference

router = APIRouter(prefix="/predict", tags=["inference"])


@router.post("", response_model=PredictionOutput)
def predict(patient: PatientInput):
    try:
        return run_inference(patient)
    except Exception as e:
        # In production, log the full exception server-side and return a
        # generic message — don't leak internals to the client.
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")
