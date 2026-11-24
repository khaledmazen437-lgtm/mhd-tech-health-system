"""
Pydantic schemas for patient input/output.

Feature order MUST match the order used when training the scaler + model:
[RIAGENDR, RIDAGEYR, BMXHT, BMXWT, SPXNFVC, SPXNFEV1, SPXNPEF]
"""

from pydantic import BaseModel, Field
from typing import Optional

class PatientInput(BaseModel):
    gender: int = Field(
        ..., ge=1, le=2, description="1 = Male, 2 = Female (matches NHANES RIAGENDR coding)"
    )
    age_years: float = Field(..., gt=0, le=120, description="RIDAGEYR")
    height_cm: float = Field(..., gt=50, le=250, description="BMXHT")
    weight_kg: float = Field(..., gt=2, le=300, description="BMXWT")
    fvc: float = Field(..., gt=0, description="SPXNFVC — Forced Vital Capacity (mL)")
    fev1: float = Field(..., gt=0, description="SPXNFEV1 — Forced Expiratory Volume in 1s (mL)")
    pef: float = Field(..., gt=0, description="SPXNPEF — Peak Expiratory Flow (mL/s)")

    class Config:
        json_schema_extra = {
            "example": {
                "gender": 1,
                "age_years": 55,
                "height_cm": 175,
                "weight_kg": 80,
                "fvc": 3800,
                "fev1": 2400,
                "pef": 6200,
            }
        }

class PredictionOutput(BaseModel):
    diagnosis: int = Field(..., description="0 = Normal, 1 = COPD")
    diagnosis_label: str
    confidence: float = Field(..., description="Model sigmoid output probability of COPD")
    fev1_fvc_ratio: float = Field(..., description="Computed FEV1/FVC ratio, for reference/audit")

class DeviceReading(BaseModel):
    """Payload the ESP32 posts once a spirometry test completes."""
    session_id: str
    fvc: float
    fev1: float
    pef: float
