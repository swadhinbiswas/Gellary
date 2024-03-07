from pydantic import BaseModel,Field
from typing import List, Optional
from model.tagmodel import TagModel

class TagBase(BaseModel):
  name:str=Field(...,description="Name of the tag")
  
class TagOut(BaseModel):
  name:Optional[str]

class TagUpadete(BaseModel):
  name:Optional[str]