import pymongo
from typing import Optional,List
from datetime import datetime
from uuid import UUID, uuid4
from schemas.imageschema import ImageBase,ImageOut,Update
from model.imagemodel import ImageModel

class ImageService:
  @staticmethod
  async def create_image(image:ImageBase)->ImageModel:
    newimage=ImageModel(
      image_id=uuid4(),
      name=image.name,
      description=image.description,
      tags=image.tags,
      image_path=image.image_path,
      thumbnail_path=image.thumbnail_path,
      created_at=datetime.now(),
      updated_at=datetime.now(),
    )
    await newimage.insert()
  
  @staticmethod
  async def get_by_imagename(imagename:str)->Optional[ImageModel]:
    theimage= await ImageModel.find_one(ImageModel.imagename==imagename)
    return theimage
  @staticmethod
  async def update_image(imagename:str,update:Update)->Optional[ImageModel]:
    image=await ImageModel.find_one(ImageModel.imagename==imagename)
    if image is None:
      raise pymongo.errors.OperationFailure("Image not found")
    await image.update({"$set":image.dict(exclude_unset=True)})
    return image
  @staticmethod
  def delete_image(imagename:str)->Optional[ImageModel]:
    image= ImageModel.find_one(ImageModel.imagename==imagename)
    if image is None:
      raise pymongo.errors.OperationFailure("Image not found")
    image.delete()
  @staticmethod
  async def get_all_images()->List[ImageModel]:
    images=await ImageModel.find().to_list()
    return images
  @staticmethod
  async def get_images_by_tag(tag:str)->List[ImageModel]:
    images=await ImageModel.find(ImageModel.tags==tag).to_list()
    return images
  @staticmethod
  async def get_images_by_tags(tags:List[str])->List[ImageModel]:
    images=await ImageModel.find(ImageModel.tags.all(tags)).to_list()
    return images
  @staticmethod 
  async def get_many(limit:int,skip:int)->List[ImageModel]:
    images=await ImageModel.find().skip(skip).limit(limit).to_list()
    return images
  @staticmethod
  async def get_by_search(search:str)->List[ImageModel]:
    images=await ImageModel.find({"$text":{"$search":search}}).to_list()
    return images
  @staticmethod
  async def select_random()->List[ImageModel]:
    images=await ImageModel.aggregate([{"$sample":{"size":1}}]).to_list()
    return images
  @staticmethod
  async def select_random_many(limit:int)->List[ImageModel]:
    images=await ImageModel.aggregate([{"$sample":{"size":limit}}]).to_list()
    return images
