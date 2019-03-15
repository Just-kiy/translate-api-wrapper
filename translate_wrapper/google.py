import aiohttp

from .engine import BaseEngine, BaseResponseConverter


class GoogleEngine(BaseEngine):
    def __init__(self, api_key, api_endpoint):
        self.api_key = api_key
        self.endpoint = api_endpoint

    async def _send_request(self, url, params):
        async with aiohttp.ClientSession() as session:
            params["key"] = self.api_key
            response = await session.post(url, params=params)
            body = await response.json()
            return GoogleResponse(response, body)

    async def translate(self, text, target, source=None, model=None):
        url = f"{self.endpoint}"
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
        url = f"{self.endpoint}/languages"
        params = {
            "target": lang,
            "model": model,
            }
        return await self._send_request(url, params)


class GoogleResponse(BaseResponseConverter):
    def __init__(self, response, body):
        super().__init__(response)
        self.body = body['data']


class GoogleServiceBuilder():
    def __init__(self):
        self._instance = None

    def __call__(self, api_key):
        if not self._instance:
            self._instance = GoogleEngine(api_key)
        return self._instance
