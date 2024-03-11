from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Any, Union
from auth.setting import setting 


password_context= CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return password_context.hash(password)
  
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)
  