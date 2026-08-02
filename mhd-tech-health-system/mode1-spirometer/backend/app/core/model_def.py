"""
Model architecture definition.

IMPORTANT: This must exactly match the architecture used in
ml-pipeline/src/model.py at training time, or state_dict loading will fail
or (worse) silently load into mismatched layers.
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
