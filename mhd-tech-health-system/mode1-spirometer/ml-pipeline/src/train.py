"""
Trains the COPD classifier on MHD_Final_Training_Data.csv, saves the
trained weights and the fitted StandardScaler for use in the backend.

Usage:
    python src/train.py
"""

import pickle
from pathlib import Path

import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from model import COPDClassifier

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "MHD_Final_Training_Data.csv"
ARTIFACTS_DIR = Path(__file__).resolve().parent.parent / "artifacts"

FEATURES = ["RIAGENDR", "RIDAGEYR", "BMXHT", "BMXWT", "SPXNFVC", "SPXNFEV1", "SPXNPEF"]
TARGET = "Diagnosis"

EPOCHS = 100
LEARNING_RATE = 0.001

def main():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES].values
    y = df[TARGET].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_t = torch.tensor(X_train_scaled, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    X_test_t = torch.tensor(X_test_scaled, dtype=torch.float32)
    y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

    model = COPDClassifier(input_size=len(FEATURES))
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    for epoch in range(EPOCHS):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train_t)
        loss = criterion(outputs, y_train_t)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 10 == 0:
            model.eval()
            with torch.no_grad():
                val_outputs = model(X_test_t)
                val_loss = criterion(val_outputs, y_test_t)
                val_preds = (val_outputs >= 0.5).float()
                val_acc = (val_preds == y_test_t).float().mean().item()
            print(
                f"Epoch {epoch + 1}/{EPOCHS} | train_loss={loss.item():.4f} "
                f"val_loss={val_loss.item():.4f} val_acc={val_acc:.4f}"
            )

    torch.save(model.state_dict(), ARTIFACTS_DIR / "mhd_spirometry_model.pth")
    with open(ARTIFACTS_DIR / "mhd_scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"Saved model + scaler to {ARTIFACTS_DIR}")

if __name__ == "__main__":
    main()
