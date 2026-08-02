# API Spec — Mode 1 Backend

Base URL (dev): `http://localhost:8000`

## `GET /health`
Returns server + model load status.

## `POST /session/start`
Called by React when the doctor clicks "Start Test", after filling demographics.

**Body:**
```json
{ "gender": 1, "age_years": 55, "height_cm": 175, "weight_kg": 80 }
```
**Response:**
```json
{ "session_id": "uuid-string" }
```

## `GET /session/{session_id}`
Polled by React while waiting on the ESP32 reading.

**Response:**
```json
{
  "session_id": "uuid-string",
  "demographics": { "...": "..." },
  "reading": null,
  "ready": false
}
```

## `POST /device/reading`
Called by the ESP32 once a spirometry test completes.

**Body:**
```json
{ "session_id": "uuid-string", "fvc": 3800, "fev1": 2400, "pef": 6200 }
```

## `POST /predict`
Runs PyTorch inference. Can be called directly, or triggered automatically by
the frontend once a session's reading is ready.

**Body:**
```json
{
  "gender": 1, "age_years": 55, "height_cm": 175, "weight_kg": 80,
  "fvc": 3800, "fev1": 2400, "pef": 6200
}
```
**Response:**
```json
{
  "diagnosis": 0,
  "diagnosis_label": "Normal",
  "confidence": 0.12,
  "fev1_fvc_ratio": 0.63
}
```
