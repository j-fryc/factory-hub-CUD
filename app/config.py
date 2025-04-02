from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    secret_key: str
    db_name: str = Field(alias="POSTGRES_DB")
    db_user: str = Field(alias="POSTGRES_USER")
    db_password: str = Field(alias="POSTGRES_PASSWORD")

    class Config:
        env_file = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
