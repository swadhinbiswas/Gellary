from model.imagemodel import ImageModel
from schemas.imageschema import ImageBase,ImageOut,Update
from services.imageservice import ImageService
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import File, UploadFile

router = APIRouter()

@router.post("/api/v1/images", summary="creatimage",response_model=ImageOut)
async def createimage(image: ImageModel):
    await ImageService.create_image(image)
    return image
  
@router.get("/api/v1/images/{imagename}", response_model=ImageOut)
async def get_image(imagename: str):
    image = await ImageService.get_by_imagename(imagename)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image
  
@router.put("/api/v1/images/{imagename}", response_model=ImageModel)
async def update_image(imagename: str, update: Update):
    image = await ImageService.update_image(imagename, update)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image
  
@router.delete("/api/v1/images/{imagename}", response_model=ImageOut)
async def delete_image(imagename: str):
    image = await ImageService.delete_image(imagename)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image
  
@router.get("/api/v1/images", response_model=List[ImageOut])
async def get_all_images():
    return await ImageService.get_all_images()
  
@router.get("/api/v1/images/tags/{tag}", response_model=List[ImageOut])
async def get_images_by_tag(tag: str):
    return await ImageService.get_images_by_tag(tag)
  
@router.get("/api/v1/images/tags", response_model=List[ImageOut])
async def get_images_by_tags(tags: List[str]):
    return await ImageService.get_images_by_tags(tags)
  
@router.get("/api/v1/images/many", response_model=List[ImageOut])
async def get_many(limit: int, skip: int):
    return await ImageService.get_many(limit, skip)
  
@router.get("/api/v1/images/search", response_model=List[ImageOut])
async def get_by_search(search: str):
    return await ImageService.get_by_search(search)
  
@router.get("/api/v1/images/random", response_model=List[ImageOut])
async def select_random():
    return await ImageService.select_random()

@router.get("/api/v1/images/random/many", response_model=List[ImageOut])
async def select_random_many(limit: int):
    return await ImageService.select_random_many(limit)
