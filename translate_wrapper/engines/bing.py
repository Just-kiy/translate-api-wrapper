import os
import typing as t

import aiohttp

from translate_wrapper.exceptions import TranslationServiceError

from .engine import BaseEngine


class BingEngine(BaseEngine):
    name = 'Bing'

    def __init__(self,
                 api_key: str,
                 api_endpoint: t.Optional[str] = None,
                 api_v: t.Optional[str] = None,
                 *,
                 event_loop=None):
        self.api_key = api_key
        self.endpoint = api_endpoint or os.getenv('BING_API_ENDPOINT')
        self.api_v = api_v or os.getenv('BING_API_V')

        self.event_loop = event_loop

    async def _send_request(self,
                            method: str,
                            url: str,
                            params: t.Optional[t.Dict[str, str]] = None,
                            body: t.Optional[t.List[t.Dict[str, str]]] = {}) -> t.Dict:
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

            body = await response.json(content_type=None)
            return body

    async def translate(self,
                        *text: str,
                        target: str,
                        source: t.Optional[str] = None) -> t.List[str]:
        """
        reference:
        https://docs.microsoft.com/ru-ru/azure/cognitive-services/translator/reference/v3-0-translate?tabs=curl
        """
        url = f'{self.endpoint}/translate'
        params = {
            'to': target,
            'textType': 'html',
        }
        if source:
            params['from'] = source
        body = []
        for line in text:
            body.append({'Text': line})
        response = await self._send_request('post', url, params, body)
        self._check_response_on_errors(response)
        return self.convert_response('translate', response)

    async def get_languages(self, *ignore) -> t.List[str]:
        """
        reference:
        https://docs.microsoft.com/ru-ru/azure/cognitive-services/translator/reference/v3-0-languages?tabs=curl
        """
        url = f'{self.endpoint}/languages'
        response = await self._send_request('get', url)
        self._check_response_on_errors(response)
        return self.convert_response('get_langs', response)

    def convert_response(self, method: str, response: t.Dict) -> t.List:
        if method == 'get_langs':
            return self._convert_langs(response)
        elif method == 'translate':
            return self._convert_translate(response)

    # TODO: staticmethod
    def _convert_langs(self, response: t.Dict) -> t.List:
        result = list(response['translation'].keys())
        return result

    def _convert_translate(self, response: t.Dict) -> t.List[str]:
        result = [item['translations'][0]['text'] for item in response]
        return result

    def _check_response_on_errors(self, response: t.Dict):
        if 'error' in response:
            raise TranslationServiceError('Bing', response['error']['code'], response['error']['message'])
