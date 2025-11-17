"""
Configuration settings for the Fraud Detection Dashboard Backend
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # App Configuration
    APP_NAME: str = "Fraud Detection Dashboard API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Data Configuration
    DATA_FILE_PATH: str = os.path.join(
        Path(__file__).parent.parent,
        "financial_fraud_detection_dataset.csv"
    )
    
    # Cache Configuration
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 300  # 5 minutes
    
    # Processing Configuration
    CHUNK_SIZE: int = 100000  # For chunked CSV reading
    MAX_WORKERS: int = 4  # For parallel processing
    
    # Real-time Configuration
    HIGH_RISK_THRESHOLD: float = 0.75  # 75% probability
    FRAUD_VELOCITY_WINDOW: int = 3600  # 1 hour in seconds
    
    # Model Configuration
    MODEL_PRECISION: float = 0.942
    MODEL_RECALL: float = 0.878
    MODEL_VERSION: str = "v2.3.1"
    
    # Alert Thresholds
    CRITICAL_FRAUD_RATE: float = 0.06  # 6%
    WARNING_FRAUD_RATE: float = 0.045  # 4.5%
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

