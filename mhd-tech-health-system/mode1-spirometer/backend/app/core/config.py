import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # .../backend

# Model artifacts live in ml-pipeline/artifacts by default so backend and
# training pipeline share the same source of truth. Override with env vars
# in production (e.g. path to a mounted volume or downloaded from S3).
MODEL_PATH = os.getenv(
    "MHD_MODEL_PATH",
    str(BASE_DIR.parent / "ml-pipeline" / "artifacts" / "mhd_spirometry_model.pth"),
)
SCALER_PATH = os.getenv(
    "MHD_SCALER_PATH",
    str(BASE_DIR.parent / "ml-pipeline" / "artifacts" / "mhd_scaler.pkl"),
)

# CORS — restrict this to your actual frontend origin(s) in production
ALLOWED_ORIGINS = os.getenv("MHD_ALLOWED_ORIGINS", "http://localhost:5173").split(",")

COPD_THRESHOLD = float(os.getenv("MHD_COPD_THRESHOLD", "0.5"))
