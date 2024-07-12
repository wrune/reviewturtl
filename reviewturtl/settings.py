from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
import dspy
from typing import Optional

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

    

def initialize_dspy_with_configs(model:Optional[str]=None,api_key:Optional[str]=None,max_tokens:Optional[int]=None):
    if model is None:
        model = "gpt-4o"
    if api_key is None:
        api_key = Settings().OPENAI_API_KEY
    if max_tokens is None:
        max_tokens = 3000
    turbo = dspy.OpenAI(
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
    )
    dspy.settings.configure(lm=turbo)

def get_settings():
    return Settings()
