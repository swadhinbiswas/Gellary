from beanie import Document
from typing import List,Any,Final

class TagModel(Document):
  name: str

  def __repr__(self) -> str:
    return f"TagModel(name={self.name})"
  
  def __str__(self) -> str:
    return self.__repr__()
  
  def __eq__(self, o: object) -> bool:
    if not isinstance(o,TagModel):
      return False
    return self.name == o.name
  
  def __ne__(self, o: object) -> bool:
    return not self.__eq__(o)
  

  @property
  def name(self) -> str:
    return self._name

    
  class Settings:
    name="tagmodel"
    