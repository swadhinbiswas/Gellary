
from typing import List
from decouple import config
from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = config('SECRET_KEY')
    PROJECT_NAME: str = config('PROJECT_NAME')
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    ALGORITHM= "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    

    class Config:
        case_sensitive = True
        
settings = Settings()
