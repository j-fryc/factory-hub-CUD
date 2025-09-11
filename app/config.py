from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    secret_key: str
    db_name: str = Field(alias="POSTGRES_DB")
    db_user: str = Field(alias="POSTGRES_USER")
    db_password: str = Field(alias="POSTGRES_PASSWORD")
    rabbitmq_host: str = Field(alias="RABBITMQ_HOST")
    rabbitmq_port: int = Field(alias="RABBITMQ_PORT")
    rabbitmq_user: str = Field(alias="RABBITMQ_USER")
    rabbitmq_password: str = Field(alias="RABBITMQ_PASSWORD")
    rabbitmq_vhost: str = Field(alias="RABBITMQ_VHOST")
    rabbitmq_queue: str = Field(alias="RABBITMQ_QUEUE")
    rabbitmq_exchange: str = Field(alias="RABBITMQ_EXCHANGE")
    rabbitmq_routing_key: str = Field(alias="RABBITMQ_ROUTING_KEY")

    class Config:
        env_file = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
