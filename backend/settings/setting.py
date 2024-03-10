
from imp import reload
from typing import List
from decouple import config
from pydantic import BaseSettings, AnyHttpUrl, validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl]
    ALGORITHM:str
    AUTH0_DOMAIN:str
    AUTH0_AUDIENCE:str
    CLIENT_URL:str
    port : int
    reload :bool 
    
    @classmethod
    @validator("CLIENT_URL","AUTH0_DOMAIN","AUTH0_AUDIENCE")
    def envtest(cls, data):
        assert data!="",f"enviroment variable {data} is not set"
        return data
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
        
settings = Settings()
