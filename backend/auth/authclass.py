from urllib.parse import urlencode,quote_plus
from fastapi import FastAPI, HTTPException,Request,Depends,status
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from pydantic_settings import BaseSettings,SettingsConfigDict
from starlette.middleware.sessions import SessionMiddleware


import http.client
from setting import settings
import asyncio

conn = http.client.HTTPSConnection(f"{settings.AUTH0_DOMAIN}")
client_id=settings.AUTH0_CLIENT_ID
client_secret=settings.AUTH0_CLINET_SECRET
audience=settings.AUTH0_AUDIENCE

async def getToken(conn,client_id,client_secret,audience)->str:
    payload = f'{{"client_id":"{client_id}","client_secret":"{client_secret}","audience":"{audience}","grant_type":"client_credentials"}}'
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    text=data.decode("utf-8")
    token=text.split('"')[3]
   
    return token

token=asyncio.run(getToken(conn,client_id,client_secret,audience))


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
      if not 'id_token' in request.session:  # it could be userinfo instead of id_token
        # this will redirect people to the login after if they are not logged in
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT, 
            detail="Not authorized",
            headers={
                "Location": "/login" 
            }
        )
      
      
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
    user:str=request.session['userinfo']
    data:str=request.session['id_token']
    session:str=request.session['access_token']
    return {"user":user,"data":data,"session":session}

      
@app.get("/profile")

def profile(request:Request):
    return request.session['userinfo']

@app.get("/login")
async def login(request:Request):
    redirect_uri=get_abs_path("callback")
    return await auth.auth0.authorize_redirect(request,redirect_uri,audience=auth0_config.audience )

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
    request.session['access_token'] = token['access_token']
    request.session['id_token'] = token['id_token']
    request.session['userinfo'] = token['userinfo']
    return RedirectResponse(url=app.url_path_for("profile"))
    
   

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)
    
 