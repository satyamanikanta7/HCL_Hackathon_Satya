from fastapi import APIRouter
from backend.routes import transactions, auth

api_router = APIRouter(prefix="/api")
api_router.include_router(transactions.router, prefix="/fraud", tags=["Fraud Detection"])
api_router.include_router(auth.router, tags=["auth"])
