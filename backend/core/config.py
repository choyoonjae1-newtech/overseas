from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./ax_oversea.db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # External APIs
    NEWSAPI_KEY: str = ""
    CALENDARIFIC_API_KEY: str = ""
    CLAUDE_API_KEY: str = ""

    # CORS (comma-separated string in .env, converted to list)
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Admin
    ADMIN_USERNAME: str = "admin"
    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "whdbswo12#"

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
