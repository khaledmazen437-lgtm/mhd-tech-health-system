"""
NHANES 2011-2012 data pipeline: merges SPX_G, DEMO_G, BMX_G on SEQN,
filters target features, labels COPD via FEV1/FVC ratio, exports clean CSV.

Usage:
    python src/preprocess.py
"""

import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

FEATURE_COLUMNS = [
    "RIAGENDR",  # Gender
    "RIDAGEYR",  # Age
    "BMXHT",     # Height
    "BMXWT",     # Weight
    "SPXNFVC",   # FVC
    "SPXNFEV1",  # FEV1
    "SPXNPEF",   # PEF
]

COPD_RATIO_THRESHOLD = 0.70


def load_xpt(filename: str) -> pd.DataFrame:
    path = RAW_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Download NHANES 2011-2012 .XPT files into "
            f"{RAW_DIR} before running this script."
        )
    return pd.read_sas(path, format="xport")


def build_dataset() -> pd.DataFrame:
    spx = load_xpt("SPX_G.XPT")
    demo = load_xpt("DEMO_G.XPT")
    bmx = load_xpt("BMX_G.XPT")

    merged = spx.merge(demo, on="SEQN", how="inner").merge(bmx, on="SEQN", how="inner")

    df = merged[["SEQN"] + FEATURE_COLUMNS].dropna(subset=FEATURE_COLUMNS)

    df["Diagnosis"] = (
        df["SPXNFEV1"] / df["SPXNFVC"] < COPD_RATIO_THRESHOLD
    ).astype(int)

    return df


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = build_dataset()
    out_path = OUT_DIR / "MHD_Final_Training_Data.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")
    print(f"Class balance:\n{df['Diagnosis'].value_counts(normalize=True)}")


if __name__ == "__main__":
    main()
