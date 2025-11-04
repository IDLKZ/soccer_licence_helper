"""
API Router configuration
Конфигурация маршрутизации API
"""
from fastapi import APIRouter
from app.presentation.api.v1.endpoints import reports

# API v1 router
api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(reports.router)

# Main API router
api_router = APIRouter()
api_router.include_router(api_v1_router)
