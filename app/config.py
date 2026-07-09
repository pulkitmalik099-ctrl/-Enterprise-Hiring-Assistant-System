from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    APP_NAME: str = "Enterprise Hiring Assistant"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "postgresql://user:password@localhost:5432/hiring_db"
    DATABASE_ECHO: bool = False

    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: Optional[str] = None

    REDIS_URL: str = "redis://localhost:6379/0"

    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MAX_UPLOAD_SIZE: int = 10485760
    ALLOWED_FILE_TYPES: List[str] = ["pdf", "docx", "doc", "txt"]
    UPLOAD_DIR: str = "./uploads"

    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()
