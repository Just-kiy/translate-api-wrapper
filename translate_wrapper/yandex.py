import os
import typing as t

import aiohttp

from .engine import BaseEngine


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
                        target: str,
                        source: t.Optional[str]) -> t.List:
        """
        reference: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
        """
        url = f'{self.endpoint}/translate'
        lang = target
        if source:
            lang = f'{source}-{target}'
        params = {
            'lang': lang,
        }
        body = {'text': text}
        response = await self._send_request(url, params, body)
        return self.convert_response('translate', response)

    async def get_langs(self, lang: str) -> t.List:
        """
        reference: https://tech.yandex.ru/translate/doc/dg/reference/getLangs-docpage/
        """
        url = f'{self.endpoint}/getLangs'
        params = {
            'ui': lang
        }
        response = await self._send_request(url, params)
        return self.convert_response('get_langs', response)

    def convert_response(self, method: str, response: t.Dict) -> t.List:
        if method == 'get_langs':
            return self._convert_langs(response)
        elif method == 'translate':
            return self._convert_translate(response)

    def _convert_langs(self, response: t.Dict) -> t.List:
        result = list(response['langs'].keys())
        return result

    def _convert_translate(self, response: t.Dict) -> t.List[str]:
        result = response['text']
        return result
