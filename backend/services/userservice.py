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