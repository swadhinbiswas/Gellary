from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder 




app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:5000",
    "http://localhost:5500",
    "http://localhost:4200",
    "http://localhost:8081",
    "http://localhost:8082",
    "http://localhost:8083",]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
    
