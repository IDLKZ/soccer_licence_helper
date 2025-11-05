"""
API V1 Router
Объединение всех роутеров API v1
"""
from fastapi import APIRouter
from app.presentation.api.v1.routers import reports, initial_reports, solutions, department_reports, certificates

api_router = APIRouter()

# Подключаем роутеры
api_router.include_router(reports.router)
api_router.include_router(initial_reports.router)
api_router.include_router(solutions.router)
api_router.include_router(department_reports.router)
api_router.include_router(certificates.router)
