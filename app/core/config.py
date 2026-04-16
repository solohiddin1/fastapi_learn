from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "ERP API"
    DEBUG: bool = True

    ALGORITHM : str

    DATABASE_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24  # 1 day
    SECRET_KEY: str

    ALLOWED_HOSTS: list[str] = ["*"]

    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str

    FASTAPI_ADMIN_SECRET: str


    class Config:
        env_file = ".env"

settings = Settings()
