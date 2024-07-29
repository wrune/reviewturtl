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
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None

    def is_dev(self):
        return self.ENVIRONMENT == Environment.Development

    def is_prod(self):
        return self.ENVIRONMENT == Environment.Production


def get_4o_token_model():
    return dspy.OpenAI(
        model="gpt-4o", api_key=Settings().OPENAI_API_KEY, max_tokens=3500
    )


def initialize_dspy_with_configs(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    max_tokens: Optional[int] = None,
    set_global: bool = True,
):
    """
    This function initializes dspy with the given model, api_key, and max_tokens.
    It returns the model wrapper object in dspy.
    Args:
        model (str, optional): The model to use. Defaults to "gpt-4o".
        api_key (str, optional): The API key to use. Defaults to the OPENAI_API_KEY from the settings.
        max_tokens (int, optional): The maximum number of tokens to use. Defaults to 3000.
    Returns:
        dspy.OpenAI: The model wrapper object in dspy.
    """
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
    # disable later , right now setting the model to the global level
    if set_global:
        dspy.settings.configure(lm=turbo)
    # this returns the model wrapper object in dspy
    return turbo


def get_settings():
    return Settings()
