from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import files, measurements
from app.core.config import settings
from app.core.logging import setup_logging
import os

setup_logging()

app = FastAPI(
    title="Geospatial File Measurement API",
    description="API for processing geospatial files and calculating measurements",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app.include_router(files.router, prefix="/api/v1")
app.include_router(measurements.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Geospatial File Measurement API",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
