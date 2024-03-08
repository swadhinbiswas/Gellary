import pymongo
from typing import Optional,List
from uuid import UUID, uuid4
from schemas.imageschema import ImageBase,ImageOut,Update
from model.imagemodel import ImageModel

class ImageService:
  @staticmethod
  async def create_image(image:ImageBase):
    image_in=ImageModel(
      imagename=image.imagename,
      imagedescription=image.imagedescription,
      imageurl=image.imageurl,
      tags=image.tags
    )
    await image_in.save()
    return image_in
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
  
  

