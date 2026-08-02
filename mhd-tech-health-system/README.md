# MHD Tech — Dual-Mode AI Healthcare System

**Founder & Software Engineer:** Mazen Khaled
**Status:** Mode 1 (Clinic) — Active | Mode 2 (ICU) — Pending PhysioNet credentialing

## Overview

MHD Tech is a dual-mode AI healthcare platform:

- **Mode 1 — Smart Spirometer (Clinic Mode, Active):** An ESP32-based IoT spirometer that measures airflow via an MPX5010DP differential pressure sensor, computes FVC/FEV1/PEF, and uses a PyTorch feedforward neural network to predict COPD from patient demographics + spirometry data.
- **Mode 2 — ICU CDSS (Pending):** A Clinical Decision Support System for mechanical ventilation, built on the MIMIC-IV dataset. Waiting on MIT PhysioNet credentialing approval.

## Architecture (Mode 1)

```
Patient blows into tube
        │
        ▼
MPX5010DP pressure sensor ──► ESP32 (computes FVC/FEV1/PEF)
        │
        ▼  HTTP POST /device/reading
FastAPI Backend ◄──────────────── React Dashboard (doctor enters demographics)
        │
        ▼  loads mhd_spirometry_model.pth + mhd_scaler.pkl
PyTorch Inference (COPD: 0/1)
        │
        ▼
Result returned to React → Green (Normal) / Red (COPD) card
```

See `docs/architecture.md` for the full diagram and `docs/api-spec.md` for endpoint contracts.

## Repo Layout

```
mode1-spirometer/
  firmware/       ESP32 C++ (PlatformIO)
  ml-pipeline/    NHANES data prep + PyTorch model training
  backend/        FastAPI inference + orchestration API
  frontend/       React + Vite + Tailwind dashboard

mode2-icu-cdss/    Scaffold only — filled in once MIMIC-IV access is granted

docs/              Architecture, API spec, credentialing status
infra/             CI/CD, reverse proxy config
```

## Quick Start (Backend)

```bash
cd mode1-spirometer/backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for interactive API docs.

## Quick Start (Frontend)

```bash
cd mode1-spirometer/frontend
npm install
npm run dev
```

## Important: Large / Binary Files

Do **not** commit these to git directly — they're gitignored:
- `mode1-spirometer/ml-pipeline/data/raw/*.XPT` (NHANES source files)
- `mode1-spirometer/ml-pipeline/artifacts/*.pth`, `*.pkl` (trained model + scaler)

Use Git LFS or pull them from cloud storage (S3/GCS) at deploy/train time. See `mode1-spirometer/ml-pipeline/README.md`.

## License

TBD — add your chosen license to `LICENSE` before making the repo public.
