import aiohttp
import typing as t
from .engine import BaseEngine, BaseResponseConverter


class YandexEngine(BaseEngine):
    def __init__(self, api_key, api_endpoint):
        self.api_key = api_key
        self.endpoint = api_endpoint

    async def _send_request(self,
                            url: str,
                            params: t.Dict[str, str],
                            body: t.Optional[t.Dict[str, str]] = None) -> t.Dict:
        async with aiohttp.ClientSession() as session:
            params['key'] = self.api_key
            response = await session.post(url, params=params, data=body)
            body = await response.json()
            return body

    async def translate(self,
                        text: str,
                        lang: str,
                        format: str = 'plain') -> t.Dict:
        url = f'{self.endpoint}/translate'
        params = {
            'lang': lang,
            'format': format,
        }
        body = {'text': text}
        return await self._send_request(url, params, body)

    async def get_langs(self, lang: str) -> t.Dict:
        url = f'{self.endpoint}/getLangs'
        params = {
            'ui': lang
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
