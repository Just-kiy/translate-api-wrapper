from .engine import BaseEngine, BaseResponseConverter
from pprint import pprint
import aiohttp

class YandexEngine(BaseEngine):
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint_api = "https://translate.yandex.net/api/v1.5/tr.json"

    async def _send_request(self, url, body=None):
        async with aiohttp.ClientSession() as session:
            response = await session.post(url, data=body)
            body = await response.json()
            return YandexResponse(response, body)


    async def translate(self, text, lang, format="plain"):
        url = f"{self.endpoint_api}/translate?key={self.api_key}&lang={lang}&format={format}"
        body = {"text": text}
        return await self._send_request(url, body)

    async def get_langs(self, lang):
        url = f"{self.endpoint_api}/getLangs?key={self.api_key}&ui={lang}"
        return await self._send_request(url)


class YandexResponse(BaseResponseConverter):
    def __init__(self, response, body):
        super().__init__(response)
        self.body = body


class YandexServiceBuilder():
    def __init__(self):
        self._instance = None

    def __call__(self, api_key):
        if not self._instance:
            self._instance = YandexEngine(api_key)
        return self._instance
