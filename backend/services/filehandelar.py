from fastapi import UploadFile,File
from fastapi.responses import FileResponse
from fastapi import APIRouter,FastAPI
from pathlib import Path
from schemas.imageschema import ImageOut
from services import imageservice

appex=FastAPI()



upload_folder = Path("backend/uploads")
"""
Routes:
    - /uploadfile/ [POST]
    - /downloadfile/{filename} [GET]
    - /listfiles/ [GET]
    - /deletefile/{filename} [DELETE]

"""


@appex.post("/uploadfile/",summary="Image Upload")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    with open(upload_folder / file.filename, "wb") as f:
        f.write(contents)
        name=file.filename
    
    return {"filename": name}

@appex.get("/downloadfile/{filename}")
async def download_file(filename: str):
    return FileResponse(upload_folder / filename)

@appex.get("/listfiles/")
async def list_files():
    return {"files": [f.name for f in upload_folder.iterdir()]}

@appex.delete("/deletefile/{filename}")
async def delete_file(filename: str):
    (upload_folder / filename).unlink()
    return {"filename": filename}


@appex.post("/createimage/",response_model=ImageOut)
async def create_image(image:ImageOut):
    return await imageservice.ImageService.create_image(image)

@appex.get("/getimage/{imagename}",response_model=ImageOut)
async def get_image(imagename:str):
    return await imageservice.ImageService.get_by_imagename(imagename)

@appex.put("/updateimage/{imagename}",response_model=ImageOut)
async def update_image(imagename:str,image:ImageOut):
    return await imageservice.ImageService.update_image(imagename,image)
@appex.delete("/deleteimage/{imagename}")
async def delete_image(imagename:str):
    return await imageservice.ImageService.delete_image(imagename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(appex, host="0.0.0.0", port=8000)