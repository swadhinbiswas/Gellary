from dataclasses import dataclass
import jwt
from setting import settings as Settings
from expreance import BadCredentialsException,UnableCredentialsException

@dataclass
class JsontoWebToken:
    jwt_access_token: str
    auth0_domain: str=f"{Settings.AUTH0_DOMAIN}/"
    auth0_audience: str=f"{Settings.AUTH0_AUDIENCE}/"
    algorithm: str=f"{Settings.ALGORITHM}"
    jwt_url=f"{auth0_domain}.well-known/jwks.json"
    
    def verify_jwt(self):
        try:
          jwt_client=jwt.PyJWKClient(jwks_uri=self.jwt_url)
          jwt_signingkey=jwt_client.get_signing_key_from_jwt(self.jwt_access_token).key
          payload=jwt.decode(self.jwt_access_token, 
                             jwt_signingkey, 
                             algorithms=[self.algorithm],
                             audience=self.auth0_audience,
                             issuer=self.auth0_domain)
          
        except jwt.exceptions.PyJWKClinetError:
          raise UnableCredentialsException
        except jwt.exceptions.PyJWTError:
          raise BadCredentialsException
        except jwt.exceptions.InvalidTokenError:
          raise BadCredentialsException
        
        return payload
      
    def validate(self):
        return self.verify_jwt()