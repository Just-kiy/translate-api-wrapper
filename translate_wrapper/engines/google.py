import os
import typing as t

import aiohttp

import logging

from translate_wrapper.exceptions import TranslationServiceError

from .engine import BaseEngine


logger = logging.getLogger('GoogleEngine')


class GoogleEngine(BaseEngine):
    def __init__(self,
                 api_key: str,
                 api_endpoint: t.Optional[str] = None,
                 *,
                 event_loop=None):
        logger.debug(f'Creating Google Engine with api key {api_key}')
        self.api_key = api_key
        self.endpoint = api_endpoint or os.getenv('GOOGLE_API_ENDPOINT')
        self.event_loop = event_loop

    async def _send_request(self,
                            url: str,
                            params: t.List[t.Tuple[str, str]]) -> t.Dict:
        logger.debug('In _send_request')
        async with aiohttp.ClientSession(loop=self.event_loop) as session:
            params.append(('key', self.api_key))
            logger.debug('Sending request to Google')
            response = await session.post(url, params=params)
            logger.debug('Retrieving json body from response')
            body = await response.json(content_type=None)
            return body

    async def translate(self,
                        *text: t.List[str],
                        target: str,
                        source: str = None) -> t.List[str]:
        """
        reference: https://cloud.google.com/translate/docs/reference/translate
        """
        logger.debug('In translate')
        url = f'{self.endpoint}'
        params = [
            ('target', target),
            ('format', 'html'),
            ]
        for line in text:
            params.append(('q', line))
        if source:
            params.append(('source', source))
        response = await self._send_request(url, params)
        self._check_response_on_errors(response)
        return self.convert_response('translate', response)

    async def get_languages(self,
                            language: str,
                            model: str = 'nmt') -> t.List[str]:
        """
        reference: https://cloud.google.com/translate/docs/reference/languages
        """
        logger.debug('In get_languages')
        url = f'{self.endpoint}/languages'
        params = [
            ('target', language),
            ('model', model),
            ]
        response = await self._send_request(url, params)
        self._check_response_on_errors(response)
        return self.convert_response('get_langs', response)

    def convert_response(self, method: str, response: t.Dict) -> t.List:
        logger.debug('In convert_response')
        if method == 'get_langs':
            return self._convert_langs(response)
        elif method == 'translate':
            return self._convert_translate(response)

    def _convert_langs(self, response: t.Dict) -> t.List:
        logger.debug('In _convert_langs')
        result = [language['language'] for language in response['data']['languages']]
        return result

    def _convert_translate(self, response: t.Dict) -> t.List[str]:
        logger.debug('In _convert_translate')
        result = [translation['translatedText'] for translation in response['data']['translations']]
        return result

    def _check_response_on_errors(self, response: t.Dict):
        logger.debug('In _check_response_on_error')
        if 'error' in response:
            raise TranslationServiceError('Google', response['error']['code'], response['error']['errors'][0])
