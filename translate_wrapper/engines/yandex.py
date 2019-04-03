import os
import typing as t

from translate_wrapper.exceptions import EngineGetLangsError, EngineTranslationError

import aiohttp

from .engine import BaseEngine


class YandexEngine(BaseEngine):
    def __init__(self,
                 api_key: str,
                 api_endpoint: t.Optional[str] = None,
                 *,
                 event_loop=None):
        self.api_key = api_key
        self.endpoint = api_endpoint or os.getenv('YANDEX_API_ENDPOINT')
        self.event_loop = event_loop

        self.error_codes = [401, 402, 404, 413, 422, 501]

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

    async def get_languages(self, lang: str) -> t.List:
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
        if 'code' in response and response['code'] in self.error_codes:
            raise EngineGetLangsError('Yandex', response['code'], response['message'])
        result = list(response['langs'].keys())
        return result

    def _convert_translate(self, response: t.Dict) -> t.List[str]:
        if 'code' in response and response['code'] in self.error_codes:
            raise EngineTranslationError('Yandex', response['code'], response['message'])
        result = response['text']
        return result