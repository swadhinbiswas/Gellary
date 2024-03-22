from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
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
import json
from urllib.parse import quote_plus, urlencode
from fastapi import Depends, FastAPI, Request, HTTPException, status
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import APIRouter
from auth2.functionals import ProtectedEndpoint, get_abs_path
from auth2.configer import settings as auth0_config
from auth2.autherregister import auther


router = APIRouter()





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

@router.get("/profile", dependencies=[Depends(ProtectedEndpoint)])
def profile(request: Request):
    """
    Profile endpoint, should only be accessible after login
    """
    return {
        "message": "Welcome to your profile",
        "userinfo": request.session['userinfo']
    
    }


@router.get("/login")
async def login(request: Request):
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    if not 'id_token' in request.session:  # it could be userinfo instead of id_token
        return await auther.auth0.authorize_redirect(
            request,
            redirect_uri=get_abs_path("callback"),
            audience=auth0_config.audience
        )
    return RedirectResponse(url=appex.url_path_for("profile"))

@router.get("/logout")
def logout(request: Request):
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    response = RedirectResponse(
        url="https://" + auth0_config.domain
            + "/v2/logout?"
            + urlencode(
                {
                    "returnTo": get_abs_path("home"),
                    "client_id": auth0_config.client_id,
                },
                quote_via=quote_plus,
            )
    )
    request.session.clear()
    return response
  
@router.get("/callback")
async def callback(request: Request):
    """
    Callback redirect from Auth0
    """
    token = await auther.auth0.authorize_access_token(request)
    userinfo = await auther.auth0.parse_id_token(request, token)
    request.session['id_token'] = token
    request.session['userinfo'] = userinfo
    return RedirectResponse(url=appex.url_path_for("profile"))


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(appex, host="0.0.0.0", port=8000)  