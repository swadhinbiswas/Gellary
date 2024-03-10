from dataclasses import dataclass
import jwt
from matplotlib.pylab import f
from Gellary.backend import auth
from settings import setting
from expreance import BadCredentialsException,UnableCredentialsException

@dataclass
class JsontoWebToken:
    jwt_access_token: str
    auth0_domain: str=f"{setting.AUTH0_DOMAIN}/"
    auth0_audience: str=setting.AUTH0_AUDIENCE
    algorithm: str=setting.ALGORITHM
    jwks=f"{auth0_domain}.well-known/jwks.json"
    
    def verify_jwt(self):
        try:
            unverified_header = jwt.get_unverified_header(self.jwt_access_token)
        except jwt.JWTError:
            raise BadCredentialsException
        if unverified_header["alg"] != "RS256":
            raise UnableCredentialsException
        return unverified_header
      