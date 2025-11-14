from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "School ERP API"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24  # 1 day

    # CORS
    ALLOWED_HOSTS: list[str] = ["*"]

    # Optional external services
    EMAIL_HOST: str = "smtp.example.com"
    EMAIL_PORT: int = 587
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    class Config:
        env_file = ".env"

# Create a single instance to import anywhere
settings = Settings()