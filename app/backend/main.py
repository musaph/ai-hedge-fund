"""FastAPI backend entry point for the AI Hedge Fund application.

This module initializes the FastAPI application, configures middleware,
and registers all API routers.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown lifecycle."""
    logger.info("Starting AI Hedge Fund backend...")
    yield
    logger.info("Shutting down AI Hedge Fund backend...")


app = FastAPI(
    title="AI Hedge Fund API",
    description="Backend API for the AI-powered hedge fund simulation platform.",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS — allow the frontend dev server and production origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
async def health_check() -> dict:
    """Return a simple health-check response."""
    return {"status": "ok", "service": "ai-hedge-fund-backend"}


@app.get("/", tags=["system"])
async def root() -> dict:
    """Root endpoint — useful for quick connectivity checks."""
    return {
        "message": "Welcome to the AI Hedge Fund API",
        "docs": "/docs",
        "redoc": "/redoc",
    }
