from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from typing import List
from model.usemodel import UseModel
from model.imagemodel import ImageModel
from schemas.imageschema import ImageBase,ImageOut,Update
from api.v1.handelars.handelars import router
from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager


async def init():
  client = AsyncIOMotorClient(
        "mongodb+srv://test1:test1@testbatch.4k43ctn.mongodb.net/?retryWrites=true&w=majority&appName=testbatch"
    )
  
  await init_beanie(database=client.test, document_models=[ImageModel])
  
  
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    try:
        yield
    finally:
        pass



app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


    
app.include_router(router,prefix="/api/v1")

  


  
  

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app,host="localhost",port=8000)
  