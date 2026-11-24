from fastapi import APIRouter, HTTPException

from app.schemas.patient import PatientInput
from app.core.session_store import create_session, get_session

router = APIRouter(prefix="/session", tags=["session"])

@router.post("/start")
def start_session(demographics: PatientInput):
    """
    Doctor fills in patient demographics in React and hits 'Start Test'.
    Returns a session_id the ESP32 firmware should be given (e.g. shown as
    a QR code, or pre-configured) so its reading can be matched back here.
    """
    session_id = create_session(demographics)
    return {"session_id": session_id}

@router.get("/{session_id}")
def poll_session(session_id: str):
    """
    React polls this endpoint after starting a session, waiting for the
    ESP32's reading to arrive. Once 'reading' is non-null, the frontend
    can trigger /predict with the combined demographics + reading data.
    """
    session = get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "demographics": session["demographics"],
        "reading": session["reading"],
        "ready": session["reading"] is not None,
    }
