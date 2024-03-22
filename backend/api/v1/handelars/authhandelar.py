import json
from urllib.parse import quote_plus, urlencode

from fastapi import Depends, FastAPI, Request, HTTPException, status
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse

from fastapi import APIRouter
from auth2.functionals import ProtectedEndpoint, get_abs_path
from auth2.configer import settings as auth0_config
from auth2.autherregister import auther


router = APIRouter()

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
    return RedirectResponse(url=app.url_path_for("profile"))

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
    return RedirectResponse(url=app.url_path_for("profile"))



