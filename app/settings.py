

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    debug: bool
    database_url: str
    echo_sql: bool = True
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: int
    
    access_token_expire_minutes: int
    access_token_secret_key: str
    algorithm: str
    
    refresh_token_expire_minutes: int
    refresh_token_secret_key: str
    
    model_config = SettingsConfigDict(env_file=".env",)
    
    
    
    
@lru_cache
def get_settings():
    return Settings() #type: ignore