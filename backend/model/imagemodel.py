from beanie import Document,Indexed
from typing import Coroutine, List,Any,Final
from datetime import datetime
from uuid import UUID,uuid4
from pydantic import Field

from pymongo.client_session import ClientSession

class ImageModel(Document):
  image_id:UUID = Field(default_factory=uuid4)
  name: str
  description: str
  tags: List[str]
  image_path: str
  thumbnail_path: str
  created_at: datetime=Field(default_factory=datetime.now)
  updated_at: datetime=Field(default_factory=datetime.now)
  
  def __repr__(self) -> str:
    return f"<ImageModel {self.tags}>"
  
  def __str__(self) -> str:
    return f"<ImageModel {self.tags}>"
  def __eq__(self, o: object) -> bool:
    if not isinstance(o, ImageModel):
      return False
    return self.image_id==o.image_id
  
  def __hash__(self) -> int:
    return hash(self.image_id)
  
  @property
  def create(self)->datetime:
    return self.created_at
  
  @classmethod
  async def getbytags(cls,tags:List[str],session:ClientSession):
    return await cls.find({"tags":{"$in":tags}}).to_list()
    
  
 
  
  class Settings:
    name="imagemodel"
  
  class Config:
    
    json_schema_extra={
      "example":{
        "name":"image",
        "description":"This is an image",
        "tags":["image","tag"],
        "image_path":"https://path/to/image",
        "thumbnail_path":"https://path/to/image/thumbnail",
        "created_at":datetime.now(),
      }
    }
    

