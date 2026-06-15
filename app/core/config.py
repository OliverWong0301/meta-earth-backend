from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "meta_earth_db"
    PROJECT_NAME: str = "Meta Earth VN Backend"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()