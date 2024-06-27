from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent


class DatabaseConfig(BaseModel):
    url: str = f"sqlite+aiosqlite:///{BASE_DIR}/OSport.sqlite3"
    echo: bool = False
    echo_pool: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict()
    api_prefix: str = "/api"
    db: DatabaseConfig = DatabaseConfig()  # Инициализация поля db



settings = Settings()



