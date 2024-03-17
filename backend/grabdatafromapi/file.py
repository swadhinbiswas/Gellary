from urllib.parse import urlencode,quote_plus
from fastapi import FastAPI, HTTPException,Request,Depends
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from pydantic_settings import BaseSettings,SettingsConfigDict
from starlette.middleware.sessions import SessionMiddleware
from a import token



app = FastAPI()

class Settings(BaseSettings):
   app_name: str = "Awesome API"
   session_secret: str=token
   domain: str="testforprojectsx.us.auth0.com"
   client_id: str="I8hJ9FE4KTxNOYl3cJAVjNSxFVWaATyK"
   client_secret: str="t37gQnVqwPy7UsBgeqZ8BBQdNMDs7pREULoRWNb9W46wNK0OIcHe3DuCkP3X7Jtd"
   audience: str="https://worker-shrill-brook-ae32.beflix.workers.dev"
   
   #model_config=SettingsConfigDict(env_file=".env",env_prefix="auth0_")
   


auth0_config=Settings()
app.add_middleware(SessionMiddleware,secret_key=auth0_config.session_secret)


auth=OAuth()
auth.register(
    "auth0",
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
    domainx=f"{app_domain}{app.url_path_for(route)}"
    print(domainx)
    return domainx
  
  
@app.get("/")
def home():
    return {"message":"Hello World"}

@app.get("/profile",dependencies=[Depends(proctect)])
def profile(request:Request):
    
  return request.session['userinfo']

      

@app.get("/login")
async def login(request:Request):
  f=auth.auth0.authorize_redirect(request,get_abs_path("callback"))
  return await f

@app.get("/logout")
def logout(request:Request):
   respose=RedirectResponse(
       url="https://"+auth0_config.domain
       +"/v2/logout?"
       +urlencode({
           "returnTo":get_abs_path("home"),
           "client_id":auth0_config.client_id,
       },
         quote_via=quote_plus
         )
   )
   request.session.clear()
   return respose


@app.get("/callback")
async def callback(request):
    token = await auth.auth0.authorize_access_token(request)
    # Store `access_token`, `id_token`, and `userinfo` in session
     
    
    
    return token

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)
    
 