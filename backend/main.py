from fastapi import FastAPI
from dotenv import load_dotenv
from backend.routes.api_router import api_router
from backend.core.config import settings
from backend.db.init_db import create_tables

load_dotenv()

create_tables()

app = FastAPI(
    title=settings.APP_NAME, description="Advanced Fraud Detection System with ML-powered anomaly detection")

# Include API routes
app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} is running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": settings.APP_NAME}
