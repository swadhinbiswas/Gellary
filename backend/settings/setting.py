from typing import List
from decouple import config
from pydantic import BaseSettings, AnyHttpUrl, validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str=config("SECRET_KEY")
    PROJECT_NAME: str=config("PROJECT_NAME")
    ALGORITHM:str=config("ALGORITHM")
    AUTH0_DOMAIN:str=config("AUTH0_DOMAIN")
    AUTH0_AUDIENCE:str=config("AUTH0_AUDIENCE")
    CLIENT_URL:str=config("CLIENT_URL")
    reload:bool=config("reload",default=True,cast=bool)
    
    @classmethod
    @validator("CLIENT_URL","AUTH0_DOMAIN","AUTH0_AUDIENCE")
    def envtest(cls, data):
        assert data!="",f"enviroment variable {data} is not set"
        return data
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
        
settings = Settings()

print(settings.API_V1_STR)