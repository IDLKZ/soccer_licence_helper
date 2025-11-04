"""
API V1 Router
Объединение всех роутеров API v1
"""
from fastapi import APIRouter
from app.presentation.api.v1.routers import reports, solutions, department_reports

api_router = APIRouter()

# Подключаем роутеры
api_router.include_router(reports.router)
api_router.include_router(solutions.router)
api_router.include_router(department_reports.router)
