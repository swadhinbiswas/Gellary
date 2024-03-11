from beanie import Document,Indexed
from typing import List,Any,Final
from datetime import datetime

from matplotlib.pylab import f

class ImageModel(Document):
  image_id: str=Indexed()
  name: str
  description: str
  tags: List[str]
  created_at: datetime
  updated_at: datetime
  image_path: str
  thumbnail_path: str

  def __repr__(self) -> str:
    return f"ImageModel(name={self.name},description={self.description},tags={self.tags},created_at={self.created_at},updated_at={self.updated_at},image_path={self.image_path},thumbnail_path={self.thumbnail_path})"
  
  def __str__(self) -> str:
    return self.__repr__()
  
  def __eq__(self, o: object) -> bool:
    if not isinstance(o,ImageModel):
      return False
    return self.name == o.name and self.description == o.description and self.tags == o.tags and self.created_at == o.created_at and self.updated_at == o.updated_at and self.image_path == o.image_path and self.thumbnail_path == o.thumbnail_path
  
  def __ne__(self, o: object) -> bool:
    return not self.__eq__(o)
  
  @property
  def id(self) -> Any:
    return self._id
  
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def description(self) -> str:
    return self._description
  
  @property
  def tags(self) -> List[str]:
    return self._tags
  
  @property
  def created_at(self) -> datetime:
    return self._created_at
  
  @property
  def updated_at(self) -> datetime:
    return self._updated_at
  
  @property
  def image_path(self) -> str:
    return self._image_path
  
  @property
  def thumbnail_path(self) -> str:
    return self._thumbnail_path
  
  @id.setter
  def id(self, value: Any):
    self._id = value
    
  @name.setter
  def name(self, value: str):
    self._name = value
    
  @classmethod
  async def get_by_title(cls, name:str ):
    return await cls.get_one({"name":name})
  @classmethod
  async def get_by_tages(cls, tags:List[str]):
    return await cls.get_many({"tags":tags})
  
  class Collection:
    name="imagemodel"

