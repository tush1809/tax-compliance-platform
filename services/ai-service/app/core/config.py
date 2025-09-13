"""
Configuration management
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    
    # Application
    app_name: str = "Tax AI Service"
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()

