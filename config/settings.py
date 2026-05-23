from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # API settings
    API_HOST: str = Field("0.0.0.0", env="API_HOST")
    API_PORT: int = Field(8000, env="API_PORT")
    DEBUG: bool = Field(False, env="DEBUG")
    
    # Database
    DATABASE_URL: str = Field("sqlite:///levels.db", env="DATABASE_URL")
    REDIS_URL: str = Field("redis://localhost:6379", env="REDIS_URL")
    
    # Rate limiting
    RATE_LIMIT_CALLS: int = Field(100, env="RATE_LIMIT_CALLS")
    RATE_LIMIT_PERIOD: int = Field(60, env="RATE_LIMIT_PERIOD")
    
    # ML Model settings
    MODEL_PATH: str = Field("./models", env="MODEL_PATH")
    TRAIN_MODELS_ON_STARTUP: bool = Field(True, env="TRAIN_MODELS_ON_STARTUP")
    
    # Monitoring
    ENABLE_METRICS: bool = Field(True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(9090, env="METRICS_PORT")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()