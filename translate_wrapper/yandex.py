from engine import BaseEngine, BaseResponseConverter
import aiohttp
import asyncio

ENDPOINT_API = "https://translate.yandex.net/api/v1.5/tr.json"

class YandexEngine(BaseEngine):
    def __init__(self, api_key):
        self.api_key = api_key

    async def _send_request(self, url, body=None):
        async with aiohttp.ClientSession() as session:
            response =  session.post(url, data=body)
            body = await response.json()
            return YandexResponse(response, body)

    def translate(self, text, lang, format="plain"):
        url = f"{ENDPOINT_API}/translate?key={self.api_key}&lang={lang}&format={format}"
        body = {"text": text}
        return self._send_request(url, body)

    def get_langs(self, lang):
        url = f"{ENDPOINT_API}/getLangs?key={self.api_key}&ui={lang}"
        return asyncio.wait(self._send_request(url))


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
