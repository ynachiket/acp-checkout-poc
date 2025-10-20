"""
Main FastAPI Application

Entry point for the Agentic Commerce POC backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.gateway.acp import routes as acp_routes
from app.mcp import server as mcp_server


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    init_db()
    yield
    # Shutdown
    pass


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for Agentic Commerce Protocol integration",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(acp_routes.router)
app.include_router(mcp_server.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Nike Agentic Commerce POC API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }

