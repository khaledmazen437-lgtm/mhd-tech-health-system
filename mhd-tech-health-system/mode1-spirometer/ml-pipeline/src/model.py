"""
Model architecture — SOURCE OF TRUTH.

backend/app/core/model_def.py mirrors this exactly. If you change this
architecture, update the backend copy too, or extract this into a shared
package both sides import from.
"""

import torch.nn as nn


class COPDClassifier(nn.Module):
    def __init__(self, input_size: int = 7):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.net(x)
