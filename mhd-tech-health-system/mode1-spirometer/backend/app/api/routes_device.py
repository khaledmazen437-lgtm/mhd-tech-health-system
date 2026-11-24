from fastapi import APIRouter, HTTPException

from app.schemas.patient import DeviceReading
from app.core.session_store import attach_reading

router = APIRouter(prefix="/device", tags=["device"])

@router.post("/reading")
def submit_reading(reading: DeviceReading):
    """
    ESP32 firmware POSTs here once a spirometry test completes, with the
    session_id it was given when the test started (see /session/start).
    """
    ok = attach_reading(reading)
    if not ok:
        raise HTTPException(status_code=404, detail="Unknown session_id")
    return {"status": "received", "session_id": reading.session_id}
