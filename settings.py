from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Tuple

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str
    DATASET_URL: str
    TAMANHO_IMG: int
    EXT:str