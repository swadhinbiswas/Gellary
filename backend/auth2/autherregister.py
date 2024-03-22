from authlib.integrations.starlette_client import OAuth
from configer import settings

auth0_config=settings
auther=OAuth()
auther.register(
    "auth0",
    client_id=auth0_config.client_id,
    client_secret=auth0_config.client_secret,
    server_metadata_url=f"https://{auth0_config.domain}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)

