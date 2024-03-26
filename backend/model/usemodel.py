from ast import In
from typing import Coroutine, List,Any,Final, Optional
from uuid import UUID,uuid4
from beanie import Document,Indexed
from pymongo.client_session import ClientSession
from pydantic import EmailStr

class UseModel(Document):
  
  user_id: UUID=Indexed(default_factory=uuid4)
  username: Indexed(str,unique=True) # type: ignore
  frist_name: Optional[str]=None
  last_name: Optional[str]=None
  email:Indexed(EmailStr,unique=True) # type: ignore
  hashed_password: str
  userpicture: Optional[str]=None
  gallary:Optional[List[str]]=None
  tags:Optional[List[str]]=None
  
  
  def __repr__(self) -> str:
    return f"UseModel(user_id={self.user_id},username={self.username},frist_name={self.frist_name},last_name={self.last_name},email={self.email},hashed_password={self.hashed_password},userpicture={self.userpicture},gallary={self.gallary},tags={self.tags})"
  
  def __str__(self) -> str:
    return self.__repr__()
  def __hash__(self) -> EmailStr:
    return hash(self.email)
  
  def __eq__(self, o: object) -> bool:
    if not isinstance(o,UseModel):
      return False
    return self.user_id == o.user_id and self.username == o.username and self.frist_name == o.frist_name and self.last_name == o.last_name and self.email == o.email and self.hashed_password == o.hashed_password and self.userpicture == o.userpicture and self.gallary == o.gallary and self.tags == o.tags
  
  @property
  def fullname(self) -> str:
    return f"{self.frist_name} {self.last_name}"
  
  @classmethod
  async def get_user_by_email(cls,email:str,session:ClientSession)->Optional['UseModel']:
    return await cls.get_one({"email":email},session=session)
  @classmethod
  async def get_user_by_username(cls,username:str,session:ClientSession)->Optional['UseModel']:
    return await cls.get_one({"username":username},session=session)
  
  class Settings:
    name="usermodel"


  