from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Fraud Detection System"
    JWT_SECRET: str = "your-super-secret-jwt-key-change-this-in-production"
    JWT_ALGO: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DB_FILE: str = "./fraud_detection.db"
    
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    ADMIN_EMAIL: str = ""
    
    MODEL_PATH: str = "ml_model/model.joblib"
    SCALER_PATH: str = "ml_model/scaler.joblib"
    ALERT_THRESHOLD: float = 0.8

    class Config:
        env_file = ".env"

settings = Settings()
