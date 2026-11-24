from app.core.model_loader import model_bundle
from app.core.config import COPD_THRESHOLD
from app.schemas.patient import PatientInput, PredictionOutput

def run_inference(patient: PatientInput) -> PredictionOutput:
    # Feature order MUST match training order exactly.
    features = [
        patient.gender,
        patient.age_years,
        patient.height_cm,
        patient.weight_kg,
        patient.fvc,
        patient.fev1,
        patient.pef,
    ]

    probability = model_bundle.predict(features)
    diagnosis = 1 if probability >= COPD_THRESHOLD else 0
    ratio = patient.fev1 / patient.fvc if patient.fvc > 0 else 0.0

    return PredictionOutput(
        diagnosis=diagnosis,
        diagnosis_label="COPD" if diagnosis == 1 else "Normal",
        confidence=round(probability, 4),
        fev1_fvc_ratio=round(ratio, 4),
    )
