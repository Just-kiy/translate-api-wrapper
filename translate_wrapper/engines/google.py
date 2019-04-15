import logging
import os
import typing as t

import aiohttp

from translate_wrapper.exceptions import TranslationServiceError

from .engine import BaseEngine

logger = logging.getLogger('GoogleEngine')


class GoogleEngine(BaseEngine):
    """
    Implementation of the Google Translation API
    https://cloud.google.com/translate/

    All documentations are here: https://cloud.google.com/translate/docs/reference/rest/
    HINT: https://developers.google.com/apis-explorer

    NOTE: Translation API is optimized for translation of short requests.
    The recommended maximum length for each request is 2K.
    Translation API will reject very large requests (with a 400 INVALID_ARGUMENT error)
    regardless of the available quota

    NOTE: If you exceed your quota, Translation API returns a 403 error.
    The error message says Daily Limit Exceeded if you exceeded the daily limit or User Rate Limit Exceeded
    if you exceeded either of the "Characters per 100 seconds" quotas.

    """
    name = 'Google'

    def __init__(self,
                 api_key: str,
                 api_endpoint: t.Optional[str] = None,
                 *,
                 event_loop=None):
        logger.debug(f'Creating {self.name} Engine with api key {api_key}')
        self.api_key = api_key
        self.endpoint = api_endpoint or os.getenv('GOOGLE_API_ENDPOINT')
        self.event_loop = event_loop

    async def _send_request(self,
                            url: str,
                            params: t.Optional[t.List[t.Tuple[str, str]]] = None,
                            body: t.Optional[t.Dict[str, str]] = None) -> t.Dict:

        logger.debug('In _send_request')
        async with aiohttp.ClientSession(loop=self.event_loop) as session:
            if not params:
                params = [('key', self.api_key)]

            logger.debug(f'Sending request to {self.name}')
            response = await session.post(url, params=params, json=body)

            logger.debug('Retrieving json body from response')
            body = await response.json(content_type=None)
            return body

    async def translate(self,
                        *text: str,
                        target: str,
                        source: str = None) -> t.List[str]:
        """
        reference: https://cloud.google.com/translate/docs/reference/translate
        APIs-explorer: https://developers.google.com/apis-explorer/#p/translate/v2/language.translations.translate
        """
        logger.debug('In translate')

        logger.debug('Making url and params')
        url = f'{self.endpoint}'
        body = {
            'target': target,
            'format': 'html'
        }

        logger.debug('Appending each given line of the text to a query')
        q = [line for line in text]
        body['q'] = q

        if source:
            logger.debug('Appending source language')
            body['source'] = source

        logger.debug(f'{self.name}: Sending request')
        response = await self._send_request(url, params=[], body=body)

        logger.debug(f'{self.name}: Checking response')
        self._check_response_on_errors(response)

        logger.debug(f'{self.name}: Converting response')
        return self.convert_response('translate', response)

    async def get_languages(self,
                            language: str,
                            model: str = 'nmt') -> t.List[str]:
        """
        reference: https://cloud.google.com/translate/docs/reference/languages
        APIs-explorer: https://developers.google.com/apis-explorer/#p/translate/v2/language.languages.list
        """
        logger.debug('In get_languages')

        logger.debug('Making url and params')
        url = f'{self.endpoint}/languages'
        params = [
            ('target', language),
            ('model', model),
            ]

        logger.debug(f'{self.name}: Sending request')
        response = await self._send_request(url, params)

        logger.debug(f'{self.name}: Checking response')
        self._check_response_on_errors(response)

        logger.debug(f'{self.name}: Converting response')
        return self.convert_response('get_langs', response)

    def convert_response(self, method: str, response: t.Dict) -> t.List:
        logger.debug('In convert_response')
        if method == 'get_langs':
            return self._convert_langs(response)
        elif method == 'translate':
            return self._convert_translate(response)

    @staticmethod
    def _convert_langs(response: t.Dict) -> t.List:
        logger.debug('In _convert_langs')
        result = [language['language'] for language in response['data']['languages']]
        return result

    @staticmethod
    def _convert_translate(response: t.Dict) -> t.List[str]:
        logger.debug('In _convert_translate')
        result = [translation['translatedText'] for translation in response['data']['translations']]
        return result

    @staticmethod
    def _check_response_on_errors(response: t.Dict):
        logger.debug('In _check_response_on_error')
        if 'error' in response:
            raise TranslationServiceError('Google', response['error']['code'], response['error']['errors'][0])
