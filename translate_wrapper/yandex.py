import aiohttp

from translate_wrapper.engine import BaseEngine, BaseResponseConverter

ENDPOINT_API = "https://translate.yandex.net/api/v1.5/tr.json"


class YandexEngine(BaseEngine):
    def __init__(self, api_key):
        self.api_key = api_key

    async def _send_request(self, url, params, body=None):
        async with aiohttp.ClientSession() as session:
            params["key"] = self.api_key
            response = await session.post(url, params=params, data=body)
            body = await response.json()
            return YandexResponse(response, body)

    async def translate(self, text, lang, format="plain"):
        url = f"{ENDPOINT_API}/translate"
        params = {
            "lang": lang,
            "format": format,
        }
        body = {"text": text}
        return await self._send_request(url, params, body)

    async def get_langs(self, lang):
        url = f"{ENDPOINT_API}/getLangs"
        params = {
            "ui": lang
        }
        return await self._send_request(url, params)


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
