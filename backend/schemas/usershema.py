from model.usemodel import UseModel
from pydantic import BaseModel,Field
from uuid import UUID, uuid4
from typing import Optional,List

class UseBase(BaseModel):
  username:str=Field(...,description="Name of the user",min_length=5,max_length=50)
  email:Optional[str]=Field(...,description="Email of the user")
  password:str=Field(...,description="Password of the user",min_length=8,max_length=50)
  userpicture:Optional[str]=Field(...,description="User picture")
  gallary:Optional[List[str]]=Field([],description="List of image ids")
  tags:Optional[List[str]]=Field([],description="List of tags")
  
class UseOut(BaseModel):
  username:str
  email:str
  userpicture:Optional[str]
  gallary:Optional[List[str]]
  tags:Optional[List[str]]
  
class Upadete(BaseModel):
  username:Optional[str]
  email:Optional[str]
  password:Optional[str]
  userpicture:Optional[str]
  gallary:Optional[List[str]]
  tags:Optional[List[str]]
  
  

