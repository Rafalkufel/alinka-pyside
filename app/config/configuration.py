import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_FILE_NAME: str = "Alinka.db"
    BASE_PATH: Path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DOCUMENTS_PATH = os.path.join(BASE_PATH, "dokumenty")
    DB_PATH = os.path.join(BASE_PATH, DB_FILE_NAME)


@lru_cache
def get_settings():
    return Settings()
