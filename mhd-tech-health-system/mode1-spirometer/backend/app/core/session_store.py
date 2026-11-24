"""
Minimal in-memory session store to correlate a doctor's patient-demographics
form (started in React) with the ESP32's sensor reading for the same test.

This is intentionally simple for the MVP. Swap for Redis or a DB table
(with TTL / expiry) once you need multi-device or multi-clinic support —
in-memory state won't survive a server restart or scale past one process.
"""

import uuid
from typing import Optional
from app.schemas.patient import PatientInput, DeviceReading

_sessions: dict[str, dict] = {}

def create_session(demographics: PatientInput) -> str:
    session_id = str(uuid.uuid4())
    _sessions[session_id] = {"demographics": demographics, "reading": None}
    return session_id

def attach_reading(reading: DeviceReading) -> bool:
    session = _sessions.get(reading.session_id)
    if session is None:
        return False
    session["reading"] = reading
    return True

def get_session(session_id: str) -> Optional[dict]:
    return _sessions.get(session_id)
