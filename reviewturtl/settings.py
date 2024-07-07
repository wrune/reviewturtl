from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    Production = "PROD"
    Development = "DEV"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    ENVIRONMENT: Environment = Environment.Development
    OPENAI_API_KEY: str = ""
    APP_NAME: str = "reviewturtl"

    def is_dev(self):
        return self.ENVIRONMENT == Environment.Development

    def is_prod(self):
        return self.ENVIRONMENT == Environment.Production


def get_settings():
    return Settings()
