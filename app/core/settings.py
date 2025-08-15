from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl


class Settings(BaseSettings):
    APP_NAME: str = "sales-mvp"
    ENV: str = "dev"
    DEBUG: bool = True
    # DB
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_MINSIZE: int = 1
    POSTGRES_MAXSIZE: int = 10
    # Celery
    CELERY_BROKER_URL: AnyUrl
    CELERY_RESULT_BACKEND: AnyUrl | None = None
    # Auth
    JWT_SECRET_KEY: str
    JWT_ALG: str = "HS256"
    JWT_EXPIRES_MIN: int = 60
    # Email (elige SendGrid o SMTP dev)
    SENDGRID_API_KEY: str | None = None
    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAIL_FROM: str = "no-reply@example.com"

settings = Settings()