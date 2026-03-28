from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str

    model_config = {"env_file": ".env"}

@lru_cache
def get_settings() -> Settings:
    return Settings()
