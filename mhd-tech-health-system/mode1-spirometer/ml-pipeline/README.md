# ML Pipeline — NHANES COPD Classifier

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 1. Get the raw data

Download these files from the [NHANES 2011-2012 cycle](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2011) and place them in `data/raw/`:

- `SPX_G.XPT` (Spirometry)
- `DEMO_G.XPT` (Demographics)
- `BMX_G.XPT` (Body Measures)

These are gitignored — do not commit them.

## 2. Build the training dataset

```bash
python src/preprocess.py
```

Produces `data/processed/MHD_Final_Training_Data.csv`.

## 3. Train the model

```bash
python src/train.py
```

Produces `artifacts/mhd_spirometry_model.pth` and `artifacts/mhd_scaler.pkl`.

**Copy or symlink these into `../backend/` deployment location** (or point `MHD_MODEL_PATH` / `MHD_SCALER_PATH` env vars at them — see `backend/app/core/config.py`).

## Important

`model.py`'s `COPDClassifier` architecture is duplicated in `backend/app/core/model_def.py` so the backend doesn't need to import the full ml-pipeline package. **If you change the architecture here, update the backend copy too**, or refactor both to import from a shared package.
