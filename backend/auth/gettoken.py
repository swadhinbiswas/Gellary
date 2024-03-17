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


