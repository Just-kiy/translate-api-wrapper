import os
import typing as t

import aiohttp

from .engine import BaseEngine


class GoogleEngine(BaseEngine):
    def __init__(self,
                 api_key: str,
                 api_endpoint: t.Optional[str] = None,
                 *,
                 event_loop=None):
        self.api_key = api_key
        self.endpoint = api_endpoint or os.getenv('GOOGLE_API_ENDPOINT')
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
        """
        reference: https://cloud.google.com/translate/docs/reference/translate
        """
        url = f'{self.endpoint}'
        params = {
            'q': text,
            'target': target,
            }
        if source:
            params['source'] = source
        return await self._send_request(url, params)

    async def get_languages(self,
                            language: str,
                            model: str = 'nmt') -> t.Dict:
        """
        reference: https://cloud.google.com/translate/docs/reference/languages
        """
        url = f'{self.endpoint}/languages'
        params = {
            'target': language,
            'model': model,
            }
        return await self._send_request(url, params)

    def convert_response(self, method: str, response: t.Dict) -> t.List:
        if method == 'get_langs':
            return self._convert_langs(response)
        elif method == 'translate':
            return self._convert_translate(response)

    def _convert_langs(self, response: t.Dict) -> t.List:
        result = [language['language'] for language in response['data']['languages']]
        return result

    def _convert_translate(self, response: t.Dict) -> t.List[str]:
        result = [translation['translatedText'] for translation in response['data']['translations']]
        return result
