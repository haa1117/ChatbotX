"""
Configuration settings for ChatBotX
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "ChatBotX - AI Support Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30, env="REFRESH_TOKEN_EXPIRE_DAYS")
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000", "https://localhost:3000"],
        env="ALLOWED_ORIGINS"
    )
    
    # Database
    MONGODB_URL: str = Field(..., env="MONGODB_URL")
    DATABASE_NAME: str = Field(default="chatbotx", env="DATABASE_NAME")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    
    # Rasa
    RASA_SERVER_URL: str = Field(default="http://localhost:5005", env="RASA_SERVER_URL")
    RASA_MODEL_PATH: str = Field(default="../rasa/models", env="RASA_MODEL_PATH")
    RASA_CONFIG_PATH: str = Field(default="../rasa/config.yml", env="RASA_CONFIG_PATH")
    
    # Email
    SMTP_TLS: bool = Field(default=True, env="SMTP_TLS")
    SMTP_PORT: Optional[int] = Field(default=None, env="SMTP_PORT")
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_USER: Optional[str] = Field(default=None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: Optional[str] = Field(default=None, env="EMAILS_FROM_EMAIL")
    EMAILS_FROM_NAME: Optional[str] = Field(default=None, env="EMAILS_FROM_NAME")
    
    # Twilio (SMS/WhatsApp)
    TWILIO_ACCOUNT_SID: Optional[str] = Field(default=None, env="TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = Field(default=None, env="TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: Optional[str] = Field(default=None, env="TWILIO_PHONE_NUMBER")
    
    # File Upload
    UPLOAD_FOLDER: str = Field(default="uploads", env="UPLOAD_FOLDER")
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=[".pdf", ".doc", ".docx", ".txt", ".png", ".jpg", ".jpeg"],
        env="ALLOWED_FILE_TYPES"
    )
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_PERIOD: int = Field(default=60, env="RATE_LIMIT_PERIOD")  # seconds
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # Analytics
    ENABLE_ANALYTICS: bool = Field(default=True, env="ENABLE_ANALYTICS")
    ANALYTICS_RETENTION_DAYS: int = Field(default=90, env="ANALYTICS_RETENTION_DAYS")
    
    # AI Features
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")
    ENABLE_SENTIMENT_ANALYSIS: bool = Field(default=True, env="ENABLE_SENTIMENT_ANALYSIS")
    ENABLE_LANGUAGE_DETECTION: bool = Field(default=True, env="ENABLE_LANGUAGE_DETECTION")
    
    # Multi-language Support
    SUPPORTED_LANGUAGES: List[str] = Field(
        default=["en", "es", "fr", "de"], 
        env="SUPPORTED_LANGUAGES"
    )
    DEFAULT_LANGUAGE: str = Field(default="en", env="DEFAULT_LANGUAGE")
    
    # Business Hours
    BUSINESS_HOURS_START: int = Field(default=9, env="BUSINESS_HOURS_START")  # 9 AM
    BUSINESS_HOURS_END: int = Field(default=17, env="BUSINESS_HOURS_END")    # 5 PM
    BUSINESS_TIMEZONE: str = Field(default="UTC", env="BUSINESS_TIMEZONE")
    
    # Education Specific
    ACADEMIC_YEAR_START: str = Field(default="2024-01-01", env="ACADEMIC_YEAR_START")
    ACADEMIC_YEAR_END: str = Field(default="2024-12-31", env="ACADEMIC_YEAR_END")
    DEFAULT_CURRENCY: str = Field(default="USD", env="DEFAULT_CURRENCY")
    
    # Integration APIs
    ZOOM_API_KEY: Optional[str] = Field(default=None, env="ZOOM_API_KEY")
    ZOOM_API_SECRET: Optional[str] = Field(default=None, env="ZOOM_API_SECRET")
    CALENDAR_API_KEY: Optional[str] = Field(default=None, env="CALENDAR_API_KEY")
    
    # Monitoring
    ENABLE_PROMETHEUS: bool = Field(default=True, env="ENABLE_PROMETHEUS")
    PROMETHEUS_PORT: int = Field(default=8001, env="PROMETHEUS_PORT")
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @validator("SUPPORTED_LANGUAGES", pre=True)
    def assemble_languages(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_FILE_TYPES", pre=True)
    def assemble_file_types(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings() 