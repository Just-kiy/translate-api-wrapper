import os
import typing as t

import aiohttp

from .engine import BaseEngine, BaseResponseConverter


class YandexEngine(BaseEngine):
    def __init__(self,
                 api_key: str,
                 api_endpoint: str,
                 *,
                 event_loop=None):
        self.api_key = api_key
        self.endpoint = api_endpoint or os.getenv('YANDEX_API_ENDPOINT')
        self.event_loop = event_loop

    async def _send_request(self,
                            url: str,
                            params: t.Dict[str, str],
                            body: t.Optional[t.Dict[str, str]] = None) -> t.Dict:
        async with aiohttp.ClientSession(loop=self.event_loop) as session:
            params['key'] = self.api_key
            response = await session.post(url, params=params, data=body)
            body = await response.json()
            return body

    async def translate(self,
                        text: str,
                        lang: str) -> t.Dict:
        url = f'{self.endpoint}/translate'
        params = {
            'lang': lang,
        }
        body = {'text': text}
        return await self._send_request(url, params, body)

    async def get_langs(self, lang: str) -> t.Dict:
        url = f'{self.endpoint}/getLangs'
        params = {
            'ui': lang
        }
        return await self._send_request(url, params)

    def convert_response(self, response: t.Dict) -> t.Dict:
        '''
        Convert response from Yandex representation to Base Schema
        :param (Dict) response: pure json containing info from server
        :return: (Dict) Base Schema Dict
        '''
        return response
