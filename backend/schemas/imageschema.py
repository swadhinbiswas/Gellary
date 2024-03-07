from typing import Optional, List, Any


from pydantic import BaseModel,EmailStr,Field
from model.imagemodel import ImageModel

class ImageBase(BaseModel):
  name:str=Field(...,description="Name of the image")
  description:str=Field(...,description="Description of the image")
  tags:List[str]=Field([],description="List of tags")
  image_path:str=Field(...,description="Path to the image")
  thumbnail_path:str=Field(...,description="Path to the thumbnail")
  
class ImageOut(BaseModel):
  name:str
  description:str
  tags:List[str]
  image_path:str
  thumbnail_path:str
  
class Update(BaseModel):
  name:Optional[str]
  description:Optional[str]
  tags:Optional[List[str]]
  image_path:Optional[str]
  thumbnail_path:Optional[str]
  
