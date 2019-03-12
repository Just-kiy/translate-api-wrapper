from .engine import BaseEngine, BaseResponseConverter
import aiohttp
import asyncio

ENDPOINT_API = "https://translation.googleapis.com/language/translate/v2"

class GoogleEngine(BaseEngine):
    def __init__(self, api_key):
        self.api_key = api_key

    async def _send_request(self, url, params):
        async with aiohttp.ClientSession() as session:
            params["key"] = self.api_key
            response =  await session.post(url, params=params)
            body = await response.json()
            return GoogleResponse(response, body)

    async def translate(self, text, target, source=None, model=None):
        url = f"{ENDPOINT_API}"
        params = {
            "q": text,
            "target": target,
            }
        if source:
            params["source"] = source
        if model:
            params["model"] = model
        return await self._send_request(url, params)

    async def get_langs(self, lang, model="nmt"):
        url = f"{ENDPOINT_API}/languages"
        params = {
            "target": lang, 
            "model": model,
            }
        return await self._send_request(url, params)


class GoogleResponse(BaseResponseConverter):
    def __init__(self, response, body):
        super().__init__(response)
        self.body = body['data']
