import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "FastAPI app"
    admin_email: str | None = os.getenv("ADMIN_EMAIL")
    admin_name: str | None = os.getenv("ADMIN_NAME")
    admin_password: str | None = os.getenv("ADMIN_PASSWORD")

    backend_url: str = os.getenv("BACKEND_URL") or "http://localhost:8000"
    otp_expriration_in_minutes: int = (
        int(os.getenv("OTP_EXPIRATION_IN_MINUTES", 10)) or 10
    )

    mail_username: str = os.getenv("MAIL_USERNAME") or "trantudev@gmail.com"
    mail_password: str = os.getenv("MAIL_PASSWORD") or "trantudev"
    mail_port: int = int(os.getenv("MAIL_PORT", 465)) or 465
    # mail_server: str = os.getenv("MAIL_SERVER") or "smtp.gmail.com"
    mail_server: str = "mail server"
    mail_starttls: bool = bool(os.getenv("MAIL_STARTTLS", False)) or False
    mail_ssl_tls: bool = bool(os.getenv("MAIL_SSL_TLS", True)) or True
    use_credentials: bool = bool(os.getenv("USE_CREDENTIALS", True)) or True
    validate_certs: bool = bool(os.getenv("VALIDATE_CERTS", True)) or True

    access_secret: str = os.getenv("JWT_SECRET") or "secret"
    access_expiration: int = (
        int(os.getenv("JWT_EXPIRATION", 60 * 60 * 24 * 7)) or 604800
    )
    refresh_secret: str = os.getenv("JWT_REFRESH_SECRET") or "refresh_secret"
    refresh_expiration: int = (
        int(os.getenv("JWT_REFRESH_EXPIRATION", 60 * 60 * 24 * 7)) or 604800
    )

    db_pass: str = os.getenv("POSTGRES_PASSWORD") or "supersecretpassword"
    db_user: str = os.getenv("POSTGRES_USER") or "user1"
    db_host: str = os.getenv("POSTGRES_HOST") or "localhost"
    db_port: int = int(os.getenv("POSTGRES_PORT", 5432)) or 5432
    db_name: str = os.getenv("POSTGRES_DB") or "fastapi_demo"

    redis_host: str = os.getenv("REDIS_HOST") or "fastapi_demo"
    redis_port: int = int(os.getenv("REDIS_PORT", 6379)) or 6379


settings = Settings()
