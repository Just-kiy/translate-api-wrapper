import os
import typing as t

import aiohttp

from translate_wrapper.exceptions import EngineGetLangsError, EngineTranslationError

from .engine import BaseEngine


class BingEngine(BaseEngine):
    def __init__(self,
                 api_key: str,
                 api_endpoint: t.Optional[str] = None,
                 api_v: t.Optional[str] = None,
                 *,
                 event_loop=None):
        self.api_key = api_key
        self.endpoint = api_endpoint or os.getenv('BING_API_ENDPOINT')
        self.api_v = api_v or os.getenv('BING_API_V_ENDPOINT')

        self.event_loop = event_loop

    async def _send_request(self,
                            method: str,
                            url: str,
                            params: t.Optional[t.Dict[str, str]] = None,
                            body: t.Optional[t.List[t.Dict[str, str]]] = None) -> t.Dict:
        async with aiohttp.ClientSession(loop=self.event_loop) as session:
            headers = {
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': self.api_key,
            }

            if not params:
                params = {}
            params['api-version'] = self.api_v

            response = await session.request(
                method=method,
                url=url,
                params=params,
                json=body,
                headers=headers
            )

            body = await response.json()
            return body

    async def translate(self,
                        text: str,
                        target: str,
                        source: t.Optional[str] = None) -> t.List[str]:
        """
        reference:
        https://docs.microsoft.com/ru-ru/azure/cognitive-services/translator/reference/v3-0-translate?tabs=curl
        """
        url = f'{self.endpoint}/translate'
        params = {
            'to': target,
        }
        if source:
            params['from'] = source
        body = [{'Text': text}]
        response = await self._send_request('post', url, params, body)
        return self.convert_response('translate', response)

    async def get_languages(self, *ignore) -> t.List[str]:
        """
        reference:
        https://docs.microsoft.com/ru-ru/azure/cognitive-services/translator/reference/v3-0-languages?tabs=curl
        """
        url = f'{self.endpoint}/languages'
        response = await self._send_request('get', url)
        return self.convert_response('get_langs', response)

    def convert_response(self, method: str, response: t.Dict) -> t.List:
        if method == 'get_langs':
            return self._convert_langs(response)
        elif method == 'translate':
            return self._convert_translate(response)

    def _convert_langs(self, response: t.Dict) -> t.List:
        if 'error' in response:
            raise EngineGetLangsError('Bing', response['error']['code'], response['error']['message'])
        result = list(response['translation'].keys())
        return result

    def _convert_translate(self, response: t.Dict) -> t.List[str]:
        if 'error' in response:
            raise EngineTranslationError('Bing', response['error']['code'], response['error']['message'])
        result = [item['translations'][0]['text'] for item in response]
        return result
