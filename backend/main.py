from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Form
from fastapi import File
from fastapi import UploadFile
from fastapi import BackgroundTasks
from fastapi import Query
from fastapi import Cookie
from fastapi import Header
from fastapi import Response
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi import Body
from fastapi import Path
from fastapi import Security
from api.v1.handelars import authhandelar




appex = FastAPI()
appex.include_router(authhandelar.router, prefix="/auth")




# appex.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

appex.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@appex.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(appex, host="0.0.0.0", port=8000)  