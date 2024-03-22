from fastapi import Request, HTTPException, status

from api.v1.app import mainapp as app

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

def get_abs_path(route: str):
    app_domain = "http://localhost:8000"
    return f"{app_domain}{app.url_path_for(route)}"
  

