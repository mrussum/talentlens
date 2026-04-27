import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.candidate import HealthResponse
from app.routes.generate import router as generate_router
from app.utils.logging import configure_logging

APP_VERSION = "1.0.0"

configure_logging()
logger = logging.getLogger("talentlens.app")

app = FastAPI(
    title="TalentLens API",
    description="AI-powered candidate assessment report generator.",
    version=APP_VERSION,
)

_allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(generate_router)


@app.get("/api/health", response_model=HealthResponse, tags=["meta"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=APP_VERSION)
