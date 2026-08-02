from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import ALLOWED_ORIGINS
from app.core.model_loader import model_bundle
from app.api import routes_inference, routes_device, routes_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model + scaler ONCE when the server starts, not per-request.
    model_bundle.load()
    yield
    # (place any cleanup here on shutdown, if ever needed)


app = FastAPI(
    title="MHD Tech — Smart Spirometer API",
    description="Serves COPD predictions from the trained PyTorch model, "
    "and coordinates data between the ESP32 device and the React dashboard.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_inference.router)
app.include_router(routes_device.router)
app.include_router(routes_session.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model_bundle.loaded}
