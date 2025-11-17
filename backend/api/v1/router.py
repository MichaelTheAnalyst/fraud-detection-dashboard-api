"""
API v1 router - Combines all endpoint routers
"""
from fastapi import APIRouter

from backend.api.v1.endpoints import dashboard, analytics, network, model_monitoring

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard - Executive & Operational"]
)

api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics & Business Intelligence"]
)

api_router.include_router(
    network.router,
    prefix="/network",
    tags=["Network Analysis & Fraud Rings"]
)

api_router.include_router(
    model_monitoring.router,
    prefix="/model",
    tags=["Model Performance Monitoring"]
)

