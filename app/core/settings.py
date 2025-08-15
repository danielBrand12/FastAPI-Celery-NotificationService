from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl


class Settings(BaseSettings):
    APP_NAME: str = "sales-mvp"
    ENV: str = "dev"
    DEBUG: bool = True
    # DB
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_MINSIZE: int = 1
    POSTGRES_MAXSIZE: int = 10
    # Broker
    CELERY_BROKER_URL: AnyUrl | None = None
    CELERY_RESULT_BACKEND: AnyUrl | None = None

    # Celery
    CELERY_BROKER_URL: AnyUrl | None = None
    CELERY_RESULT_BACKEND: AnyUrl | None = None
    # Auth
    JWT_SECRET_KEY: str | None = None
    JWT_ALG: str = "HS256"
    JWT_EXPIRES_MIN: int = 60
    # Email (elige SendGrid o SMTP dev)
    SENDGRID_API_KEY: str | None = None
    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAIL_FROM: str = "no-reply@example.com"

    CREATE_DEFAULT_DATA: bool = True

settings = Settings()