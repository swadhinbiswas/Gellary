from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from decouple import config
from typing import List

class Settings(BaseSettings):
    API_V1_STR:str="api/v1"
    SECRET_KEY:str=config("SECRETKEY",cast=str)
    SECRET_KEY: str=config("SECRET_KEY",cast=str)
    DATABASE_URL: str=config("DATABASE_URL",cast=str)
    DATABASEPASSWORD: str=config("DATABASEPASSWORD",cast=str)
    DATABASEUSER: str=config("DATABASEUSER",cast=str)
    DATABASENAME: str=config("DATABASENAME",cast=str)
    DATABASEPORT: str=config("DATABASEPORT",cast=str)
    CACHED_DATABASE_URL: str=config("CACHED_DATABASE_URL",cast=str)
    CACHED_DATABASEPASSWORD: str=config("CACHED_DATABASEPASSWORD",cast=str)
    CACHED_DATABASEUSER: str=config("CACHED_DATABASEUSER",cast=str)
    CACHED_DATABASENAME: str=config("CACHED_DATABASENAME",cast=str)
    CACHED_DATABASEPORT: str=config("CACHED_DATABASEPORT",cast=str)
    APPNAME: str = ""
    PROJECT_NAME: str=config("PROJECT_NAME",cast=str)
    ALGORITHM:str=config("ALGORITHM",cast=str)
    AUTH0_DOMAIN:str=config("AUTH0_DOMAIN",cast=str)
    AUTH0_CLIENT_ID:str=config("AUTH0_CLIENT_ID",cast=str)
    AUTH0_CLINET_SECRET:str=config("AUTH0_CLINET_SECRET",cast=str)
    AUTH0_AUDIENCE:str=config("AUTH0_AUDIENCE",cast=str)
    CLIENT_URL:str=config("CLIENT_URL",cast=str)
    SSL_CONTEXT:str=config("SSL_CONTEXT",cast=str)
    SSLPATH:str=config("SSLPATH",cast=str)
    SSLKEYPATH:str=config("SSLKEYPATH",cast=str)
    reload:bool=config("reload",default=True,cast=bool)
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive=True
        
settings=Settings()