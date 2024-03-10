from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder 
import secure 
from settings.setting import settings
from starlette.exceptions import HTTPException as StarletteHTTPException






app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    
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



@app.get('/api/test/')
async def root():
    return {"message": "Hello World"}





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, 
                host="localhost",
                port=8000,

                server_header=False)
    
