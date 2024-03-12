from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import secure 
from auth.dependency import valid_token
from auth.setting import settings
from starlette.exceptions import HTTPException as StarletteHTTPException






app = FastAPI(
    description="Photo Doc"
)

csp=secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
hsts=secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
referrer=secure.ReferrerPolicy().no_referrer()
cache_value=secure.CacheControl().no_cache().no_store().must_revalidate()
x_frame=secure.XFrameOptions().deny()


secure_headers = secure.Secure(
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    cache=cache_value,
    xfo=x_frame,
    
    
)

@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Accept-Encoding", "Accept-Language", "Origin", "Referer", "User-Agent", "X-Requested-With", "X-CSRF-Token", "X-CSRFToken", "X-XSRF-TOKEN"],
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    message = str(exc.detail)

    return JSONResponse({"message": message}, status_code=exc.status_code)



@app.get("/api")
async def read_root():
    return {"text": "This is a protected message.",
            "message": "Hello World",
            "status": "ok",
            "description": "This is a protected message."}

@app.get("/api/messages/protected", dependencies=[Depends(valid_token)])
def protected():
    return {"message": "This is a protected message."}
    



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, 
                host="localhost",
                port=8000,)
    
    
