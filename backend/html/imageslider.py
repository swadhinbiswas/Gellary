from fastapi import APIRouter
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

router = FastAPI()



@router.get("/html/elements/imageslider", responses={200: {"content": {"text/html": {}}}})
async def get_html_imageslider():
   
    
    
    return HTMLResponse(
        )
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(router, host="localhost", port=8000)