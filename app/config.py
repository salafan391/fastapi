from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from dotenv import find_dotenv, load_dotenv
import os


load_dotenv()

class Settings(BaseSettings):
    database_hostname:str
    port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    class Config:
        env_file = '.env'
settings = Settings()




