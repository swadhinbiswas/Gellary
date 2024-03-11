from typing import List
from auth.auth_hader import get_bearer_token
from auth.json_web_token import JsontoWebToken
from auth.expreance import PermissionDeniedException
from fastapi import Depends

def valid_token(token: str = Depends(get_bearer_token)):
  return JsontoWebToken(token).validate()

class PermissionValidation:
  def __init__(self,permission:List[str]):
    self.permission = permission 
  
  def __call__(self,token: str = Depends(valid_token)):
    token_permission = token.get("permissions")
    token_permission = set(token_permission)
    permission = set(self.permission)
    if not permission.issubset(token_permission):
      raise PermissionDeniedException


