from translate_wrapper.engine import BaseEngine, BaseResponseConverter
import aiohttp
import asyncio

ENDPOINT_API = "https://api.cognitive.microsofttranslator.com"
API_V = "3.0"


class BingEngine(BaseEngine):
    def __init__(self, api_key):
        self.api_key = api_key

    async def _send_request(self, method, url, params=None, body=None):
        async with aiohttp.ClientSession() as session:

            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Content-Type": "application/json",
            }

            if not params:
                params = {}
            params["api_version"] = API_V

            response = await session.request(
                method=method,
                url=url,
                params=params,
                data=body,
            )

            body = await response.json()
            return BingResponse(response, body)

    async def translate(self, text, target, source=None, format="plain"):
        url = f"{ENDPOINT_API}/translate"
        params = {
            "target": target,
            "format": format,
        }
        if source:
            params["source"] = source
        body = {"text": text}
        return await self._send_request("post", url, params, body)

    async def get_langs(self, lang):
        url = f"{ENDPOINT_API}/languages"
        return await self._send_request('get', url)


class BingResponse(BaseResponseConverter):
    def __init__(self, response, body):
        super().__init__(response)
        self.body = body


class BingServiceBuilder():
    def __init__(self):
        self._instance = None

    def __call__(self, api_key):
        if not self._instance:
            self._instance = BingEngine(api_key)
        return self._instance
