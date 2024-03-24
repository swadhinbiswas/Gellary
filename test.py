from fastapi import UploadFile,File
from fastapi.responses import FileResponse
from fastapi import FastAPI



appex=FastAPI()

@appex.get("/")
async def read_root():
    return {"Hello": "World"}

@appex.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@appex.get("/downloadfile/")
async def download_file():
    file_path = "file.txt"
    return FileResponse(file_path, media_type="application/octet-stream",filename="file.txt")




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(appex, host="0.0.0.0", port=8000)