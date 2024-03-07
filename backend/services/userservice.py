from typing import Optional,List 
from uuid import UUID, uuid4
from schemas.usershema import UseBase,UseOut,Upadete
from model.usemodel import UseModel
import pymongo

class UserService:
  @staticmethod
  async def create_user(user:UseBase):
    user_in=UseModel(
      username=user.username,
      email=user.email,
      hashed_password=user.password,
      userpicture=user.userpicture,
      gallary=user.gallary,
      tags=user.tags
    )
    await user_in.save()
    return user_in
  @staticmethod
  async def get_by_username(username:str)->Optional[UseModel]:
   theuser= await UseModel.find_one(UseModel.username==username)
   return theuser
 
  @staticmethod
  async def get_by_email(email:str)->Optional[UseModel]:
   themailer= await UseModel.find_one(UseModel.email==email)
   return themailer
  @staticmethod
  async def update_user(username:str,update:Upadete)->Optional[UseModel]:
    user=await UseModel.find_one(UseModel.username==username)
    if user is None:
      raise pymongo.errors.OperationFailure("User not found")
    await user.update({"$set":user.dict(exclude_unset=True)})
    
    return user
  
  