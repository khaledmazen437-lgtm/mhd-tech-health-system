"""
Loads the trained PyTorch model + sklearn scaler ONCE at app startup.

Loading per-request would add unnecessary latency and disk I/O on every
inference call — this module is imported once and reused across requests.
"""

import pickle
import torch

from app.core.config import MODEL_PATH, SCALER_PATH
from app.core.model_def import COPDClassifier

class ModelBundle:
    def __init__(self):
        self.model: COPDClassifier | None = None
        self.scaler = None
        self.loaded = False

    def load(self):
        self.model = COPDClassifier(input_size=7)
        self.model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
        self.model.eval()

        with open(SCALER_PATH, "rb") as f:
            self.scaler = pickle.load(f)

        self.loaded = True

    def predict(self, features: list[float]) -> float:
        """features: [gender, age, height, weight, fvc, fev1, pef] -> P(COPD)"""
        if not self.loaded:
            raise RuntimeError("Model not loaded. Call load() at startup.")

        scaled = self.scaler.transform([features])
        with torch.no_grad():
            tensor_input = torch.tensor(scaled, dtype=torch.float32)
            output = self.model(tensor_input)
            return float(output.item())

# Singleton instance imported across the app
model_bundle = ModelBundle()
