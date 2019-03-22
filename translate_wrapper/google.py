import typing as t

import aiohttp

from .engine import BaseEngine, BaseResponseConverter


class GoogleEngine(BaseEngine):
    def __init__(self,
                 api_key: str,
                 api_endpoint: str,
                 *,
                 event_loop=None):
        self.api_key = api_key
        self.endpoint = api_endpoint
        self.event_loop = event_loop

    async def _send_request(self,
                            url: str,
                            params: t.Dict[str, str]) -> t.Dict:
        async with aiohttp.ClientSession(loop=self.event_loop) as session:
            params['key'] = self.api_key
            response = await session.post(url, params=params)
            body = await response.json()
            return body

    async def translate(self,
                        text: str,
                        target: str,
                        source: str = None) -> t.Dict:
        url = f'{self.endpoint}'
        params = {
            'q': text,
            'target': target,
            }
        if source:
            params['source'] = source
        return await self._send_request(url, params)

    async def get_langs(self,
                        language: str,
                        model: str = 'nmt') -> t.Dict:
        url = f'{self.endpoint}/languages'
        params = {
            'target': language,
            'model': model,
            }
        return await self._send_request(url, params)


class GoogleResponse(BaseResponseConverter):
    def __init__(self, response, body):
        super().__init__(response)
        self.body = body['data']


class GoogleServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, api_key):
        if not self._instance:
            self._instance = GoogleEngine(api_key)
        return self._instance
