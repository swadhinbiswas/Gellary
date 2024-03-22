from typing import List
from decouple import config
from pydantic_settings import BaseSettings

from pydantic import validator,AnyHttpUrl


class Settings(BaseSettings):
    API_V1_STR:str="api/v1"
    
    SECRET_KEY: str=config("SECRET_KEY",cast=str)
    app_name: str = "Awesome API"
    PROJECT_NAME: str=config("PROJECT_NAME",cast=str)
    ALGORITHM:str=config("ALGORITHM",cast=str)
    AUTH0_DOMAIN:str=config("AUTH0_DOMAIN",cast=str)
    AUTH0_CLIENT_ID:str=config("AUTH0_CLIENT_ID",cast=str)
    AUTH0_CLINET_SECRET:str=config("AUTH0_CLINET_SECRET",cast=str)
    AUTH0_AUDIENCE:str=config("AUTH0_AUDIENCE",cast=str)
    CLIENT_URL:str=config("CLIENT_URL",cast=str)
    BACKEND_CORS_ORIGINS:List[AnyHttpUrl]=["http://localhost:3000", "https://amrpakhi.com", "http://localhost:8000"]
    reload:bool=config("reload",default=True,cast=bool)
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive=True
        
settings=Settings()

