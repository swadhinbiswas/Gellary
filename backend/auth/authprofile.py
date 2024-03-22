import json
from urllib.parse import quote_plus, urlencode

from fastapi import Depends, FastAPI, Request, HTTPException, status
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
templates = Jinja2Templates(directory="templates")


""" Hi! These comments are here to help you understand how to set up
The backend side of FastAPI for your WebAPP

You should've an .env file with the following format

AUTH0_SESSION_SECRET=<secret>
AUTH0_DOMAIN=<domain>
AUTH0_CLIENT_ID=<client id>
AUTH0_CLIENT_SECRET=<client secret>
AUTH0_AUDIENCE=<audience>

This file will be read by the `Settings` class below
"""

# Read and save Auth0 Configuration
class Settings(BaseSettings):
    app_name: str = "FastAPI with Auth0 Auth"
    session_secret: str="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFiNjdBZlVtczdYSkVGemQtaWpsNiJ9.eyJpc3MiOiJodHRwczovL3Rlc3Rmb3Jwcm9qZWN0c3gudXMuYXV0aDAuY29tLyIsInN1YiI6Ikk4aEo5RkU0S1R4Tk9ZbDNjSkFWak5TeEZWV2FBVHlLQGNsaWVudHMiLCJhdWQiOiJodHRwczovL3dvcmtlci1zaHJpbGwtYnJvb2stYWUzMi5iZWZsaXgud29ya2Vycy5kZXYiLCJpYXQiOjE3MTA4NTkwMTgsImV4cCI6MTcxMDk0NTQxOCwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoiSThoSjlGRTRLVHhOT1lsM2NKQVZqTlN4RlZXYUFUeUsifQ.gSkW9fDYwRwP4C2n9G4KnTtc1-pwuEVeXFVyCb4XV-ZfaoOOcDZLM2pnEw9QjUclBsc8om4X9JLJBPRIIoULUQ6GWauza99B-VL2d_LAIYkTFliv92PDjaJxHrJ-PVD-YiummbR4UWZCKhTvfboGfeVeqR83lBGxLgcZLW-sZIb2OPV5UYYGIVjDhJoPOSwzsEmXQmzlylOjwYHDrh5O083TETE4TGlOhxTjaJ2r1Jju4_VZH2RCgYUidYhtd9ePSvqtSl7a6IVikb8tYe0OzG-wHeWByBUg7Ex7S6MB5vIXcFwf_7F08oEK1uryemrwJdhQ7P9ioXkmjALOp5YSgw"
    domain: str="testforprojectsx.us.auth0.com"
    client_id: str="I8hJ9FE4KTxNOYl3cJAVjNSxFVWaATyK"
    client_secret: str="t37gQnVqwPy7UsBgeqZ8BBQdNMDs7pREULoRWNb9W46wNK0OIcHe3DuCkP3X7Jtd"
    audience: str="https://worker-shrill-brook-ae32.beflix.workers.dev"

    # model_config = SettingsConfigDict(env_file=".env", env_prefix='auth0_')

"""Storing the configuration into the `auth0_config` variable for later usage"""
auth0_config = Settings()

"""You need this to save temporary code & state in session"""
app.add_middleware(SessionMiddleware, secret_key=auth0_config.session_secret)

"""
Since you have a WebApp you need OAuth client registration so you can perform
authorization flows with the authorization server
"""
# Set up authlib OAuth provider
oauth = OAuth()
oauth.register(
    "auth0",
    client_id=auth0_config.client_id,
    client_secret=auth0_config.client_secret,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{auth0_config.domain}/.well-known/openid-configuration'
)

"""
This Dependency protects an endpoint and it can only be accessed if the user has an active session
"""
def ProtectedEndpoint(request: Request):
    if not 'id_token' in request.session:  # it could be userinfo instead of id_token
        # this will redirect people to the login after if they are not logged in
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT, 
            detail="Not authorized",
            headers={
                "Location": "/login" 
            }
        )

"""This function is used to programatically create the URLs for callback"""
def get_abs_path(route: str):
    app_domain = "http://localhost:8000"
    return f"{app_domain}{app.url_path_for(route)}"


@app.get("/")
def home(request: Request):
    """home endpoint"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@app.get("/profile", dependencies=[Depends(ProtectedEndpoint)])
def profile(request: Request):
    """
    Profile endpoint, should only be accessible after login
    """
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "userinfo": request.session['userinfo'],
            "formatted_userinfo": json.dumps(request.session['userinfo'], default=lambda o: o.__dict__, indent=4)
        }
    )


@app.get("/login")
async def login(request: Request):
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    if not 'id_token' in request.session:  # it could be userinfo instead of id_token
        return await oauth.auth0.authorize_redirect(
            request,
            redirect_uri=get_abs_path("callback"),
            audience=auth0_config.audience
        )
    return RedirectResponse(url=app.url_path_for("profile"))


@app.get("/logout")
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


@app.get("/callback")
async def callback(request: Request):
    """
    Callback redirect from Auth0
    """
    token = await oauth.auth0.authorize_access_token(request)
    # Store `access_token`, `id_token`, and `userinfo` in session
    request.session['access_token'] = token['access_token']
    request.session['id_token'] = token['id_token']
    request.session['userinfo'] = token['userinfo']
    return RedirectResponse(url=app.url_path_for("profile"))