from typing import Optional
from model.tagmodel import TagModel
from schemas.tagshema import TagBase,TagOut,TagUpadete
import pymongo 


class TagService:
  @staticmethod
  async def create_tag(tag:TagBase):
    tag_in=TagModel(
      tagname=tag.tagname,
      tagdescription=tag.tagdescription
    )
    await tag_in.save()
    return tag_in
  @staticmethod
  async def get_by_tagname(tagname:str)->Optional[TagModel]:
    thetag= await TagModel.find_one(TagModel.tagname==tagname)
    return thetag
  @staticmethod
  async def update_tag(tagname:str,update:TagUpadete)->Optional[TagModel]:
    tag=await TagModel.find_one(TagModel.tagname==tagname)
    if tag is None:
      raise pymongo.errors.OperationFailure("Tag not found")
    await tag.update({"$set":tag.dict(exclude_unset=True)})
    return tag
  
  
 