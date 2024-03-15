from urllib.parse import urlencode,quote_plus
from fastapi import FastAPI, HTTPException,Request,Depends
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse
from pydantic_settings import BaseSettings,SettingsConfigDict
from starlette.middleware.sessions import SessionMiddleware



app = FastAPI()

class Settings(BaseSettings):
   app_name: str = "Awesome API"
   session_secret: str="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFiNjdBZlVtczdYSkVGemQtaWpsNiJ9.eyJpc3MiOiJodHRwczovL3Rlc3Rmb3Jwcm9qZWN0c3gudXMuYXV0aDAuY29tLyIsInN1YiI6IjB4T1owYlFENUZZWm5QcWhudnlNbU9YbEZ4RktnbFZQQGNsaWVudHMiLCJhdWQiOiJodHRwczovL3N3YWRoaW4ubXkuaWQvYXBpIiwiaWF0IjoxNzEwNTAwNjU1LCJleHAiOjE3MTA1ODcwNTUsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IjB4T1owYlFENUZZWm5QcWhudnlNbU9YbEZ4RktnbFZQIiwicGVybWlzc2lvbnMiOltdfQ.K8LfPg-1d4FelOsGLdr0_QS0tKZUlMotugI_zb20mEuF1Ql12Btx9rlxbYcTn2g-Hg7VYkMdK4Qw8fq9B_LelZVgcevGXqn6r6m42AKb4xCCzBUglWbgog0LQT2ogaYSRWsjrh6OorOfD-hG5Mfzpu-Gn8U92EkZYpIbPfdCvElssf-OLDOLGa2WrcP4eWpLMU26EUEX6DFCG_sJLb3ZhMC3UIYIj21vjntg2Pvs_4GYMBSLe2iG79QbB5VskD0Phq_qjn99oTePK3f0vfQy68OUt0xb7tb0ciYOKaELBS2b9n4hQpHAvGcVpD_czkbfX99H78padGJqPRJ06EdF4Q"
   domain: str="testforprojectsx.us.auth0.com"
   client_id: str="0xOZ0bQD5FYZnPqhnvyMmOXlFxFKglVP"
   client_secret: str="aJTFI-G-I6pyd2r5pnKMTCEKyNgAztTb-F_5hAhEIVfA-rHcKVudsXlUhlopdDAd"
   audience: str="https://swadhin.my.id/api"
   
   #model_config=SettingsConfigDict(env_file=".env",env_prefix="auth0_")
   


auth0_config=Settings()
app.add_middleware(SessionMiddleware,secret_key=auth0_config.session_secret)


authx=OAuth()
authx.register(
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
      return request.session['token']['userinfo']

      

@app.get("/login")
async def login(request:Request):
  f=authx.auth0.authorize_redirect(request,get_abs_path("login"))
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
    token=await auth.auth0.authorize_access_token(request)
    user=await auth.auth0.parse_id_token(request,token)
    
    request.session['token']=token
    
    return RedirectResponse(url=app.url_path_for("profile"))

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)
    
    
    """
    
    
    https://testforprojectsx.us.auth0.com/authorize?response_type=code&client_id=0xOZ0bQD5FYZnPqhnvyMmOXlFxFKglVP&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcallback&scope=openid+profile+email&state=TW9lIZYEsdESDppVodQE72wdT4j77p&audience=https%3A%2F%2Fswadhin.my.id%2Fapi&nonce=kJcF7V9renvLnCA4ap8F
    
    
    
    
    
    https://testforprojectsx.us.auth0.com/authorize?response_type=code&client_id=0xOZ0bQD5FYZnPqhnvyMmOXlFxFKglVP&redirect_uri=%2Fcallback&scope=openid+profile+email&state=iiXrFdF0AQ5hdifw2ZZY9YVS83p5aX&audience=https%3A%2F%2Fswadhin.my.id%2Fapi&nonce=RdpuWgjWmdUF9N6FyPC6
    
    
    
    """