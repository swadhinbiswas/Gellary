from urllib.parse import urlencode,quote_plus
from fastapi import FastAPI, HTTPException,Request,Depends
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from pydantic_settings import BaseSettings,SettingsConfigDict
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()

class Settings(BaseSettings):
   app_name: str = "Awesome API"
   session_secret: str
   domain: str
   clinet_id: str
   client_secret: str
   audience: str
   
   model_config=SettingsConfigDict(env_file=".env",env_prefix="auth0_")
   


auth0_config=Settings()
app.add_middleware(SessionMiddleware,secret_key=auth0_config.session_secret)


auth=OAuth()
auth.register(
    name="auth0",
    client_id=auth0_config.client_id,
    client_secret=auth0_config.client_secret,
    server_metadata_url=f"https://{auth0_config.domain}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)

def proctect(request:Request):
    if not 'token' in request.session:
        raise HTTPException(status_code=403,detail="Unauthenticated")
      
      
def get_abs_path(route:str):
    app_domain="http://localhost:8000"
    
    return f"{app_domain}{app.url_path_for(route)}"
  
  
@app.route("")
def home():
    return {"message":"Hello World",
            "login":get_abs_path("login"),
            "logout":get_abs_path("logout"),
            "profile":get_abs_path("profile")
            }
  
      

@app.route("/login")
async def login(request:Request):
  return await auth.auth0.authorize_redirect(request,
                                             get_abs_path("callback"),
                                             audience=auth0_config.audience,
                                             )
  