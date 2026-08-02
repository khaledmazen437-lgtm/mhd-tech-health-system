# Architecture

## Mode 1 — Smart Spirometer (Active)

```
┌─────────────┐     pressure      ┌────────────┐   HTTP POST   ┌──────────────────┐
│ MPX5010DP   │ ────────────────► │   ESP32    │ ─────────────►│  FastAPI Backend  │
│ (sensor)    │                   │ (firmware) │  /device/     │  /device/reading  │
└─────────────┘                   └────────────┘  reading      │  /predict         │
                                                                 │  /session/*       │
┌─────────────┐    demographics   ┌────────────┐   HTTP        │                   │
│   Doctor    │ ────────────────► │   React    │ ─────────────►│  loads .pth+.pkl  │
│  (browser)  │ ◄──────────────── │ Dashboard  │ ◄─────────────│  PyTorch inference│
└─────────────┘   diagnosis card  └────────────┘   diagnosis   └──────────────────┘
```

**Data flow, step by step:**
1. Doctor fills in patient demographics in React → `POST /session/start` → gets `session_id`.
2. Patient blows into the spirometer. ESP32 computes FVC/FEV1/PEF and `POST /device/reading` with the `session_id`.
3. React polls `GET /session/{id}` until `ready: true`.
4. React combines demographics + reading, calls `POST /predict`.
5. Backend scales input with `mhd_scaler.pkl`, runs the PyTorch model, returns diagnosis + confidence.
6. React renders green (Normal) or red (COPD) result card.

## Mode 2 — ICU CDSS (Pending)

Not yet designed in detail — blocked on PhysioNet/MIMIC-IV credentialing (see `mimic-iv-status.md`). Expected to follow the same layered pattern (data pipeline → model → backend → frontend) once data access is granted, but ventilation-specific and likely with a different (probably time-series / sequence) model architecture given MIMIC-IV's structure.
