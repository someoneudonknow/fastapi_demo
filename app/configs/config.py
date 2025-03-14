import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "FastAPI app"
    admin_email: str | None = os.getenv("ADMIN_EMAIL")
    admin_name: str | None = os.getenv("ADMIN_NAME")
    admin_password: str | None = os.getenv("ADMIN_PASSWORD")
    db_pass: str = os.getenv("POSTGRES_PASSWORD") or "supersecretpassword"
    db_user: str = os.getenv("POSTGRES_USER") or "user1"
    db_host: str = os.getenv("POSTGRES_HOST") or "localhost"
    db_port: int = int(os.getenv("POSTGRES_PORT", 5432)) or 5432
    db_name: str = os.getenv("POSTGRES_DB") or "fastapi_demo"
    redis_host: str = os.getenv("REDIS_HOST") or "fastapi_demo"
    redis_port: int = int(os.getenv("REDIS_PORT", 6379)) or 6379

    # model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
