# Mode 2 — ICU CDSS (Pending)

**Status:** Blocked on MIT PhysioNet credentialing for MIMIC-IV access. See `../docs/mimic-iv-status.md`.

## Planned Scope

A Clinical Decision Support System for mechanical ventilation, built on MIMIC-IV. Once data access is granted, this directory should mirror `mode1-spirometer/`'s structure:

```
mode2-icu-cdss/
  ml-pipeline/    MIMIC-IV extraction, feature engineering, model training
  backend/        FastAPI inference API
  frontend/       Clinician-facing dashboard
```

## Notes to fill in once scoping begins

- Which ventilation parameters / MIMIC-IV tables are in scope (e.g. `chartevents`, `inputevents`, `procedureevents`)?
- What decision(s) is the CDSS supporting — e.g. weaning readiness, parameter adjustment suggestions, alerting?
- Model type: given MIMIC-IV's time-series nature, likely a sequence model (LSTM/Transformer) rather than the feedforward network used in Mode 1.
