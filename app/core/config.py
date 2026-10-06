from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./geospatial.db"
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 50
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
