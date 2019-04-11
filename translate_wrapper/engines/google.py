import logging
import os
import typing as t

import aiohttp

from translate_wrapper.exceptions import TranslationServiceError

from sys import getsizeof

from .engine import BaseEngine

logger = logging.getLogger('GoogleEngine')


class GoogleEngine(BaseEngine):
    """
    TODO:
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
                            params: t.List[t.Tuple[str, str]]) -> t.Dict:
        logger.debug('In _send_request')
        async with aiohttp.ClientSession(loop=self.event_loop) as session:
            params.append(('key', self.api_key))
            header = {
                'Content-Length': '0'
            }

            logger.debug(f'Sending request to {self.name}')
            response = await session.post(url, params=params, headers=header)

            logger.debug('Retrieving json body from response')
            try:
                body = await response.json(content_type=None)
                return body
            except Exception as exc:
                print(await response.text())
                from pprint import pprint
                pprint(params)

            # TODO: Error 411 (Length Required)!!


    async def translate(self,
                        *text: str,
                        target: str,
                        source: str = None) -> t.List[str]:
        """
        reference: https://cloud.google.com/translate/docs/reference/translate
        """
        logger.debug('In translate')

        logger.debug('Making url and params')
        url = f'{self.endpoint}'
        params = [
            ('target', target),
            ('format', 'html'),
        ]

        logger.debug('Appending each given line of the text to a query')
        for line in text:
            params.append(('q', line))

        if source:
            logger.debug('Appending source language')
            params.append(('source', source))

        logger.debug(f'{self.name}: Sending response')
        response = await self._send_request(url, params)

        logger.debug(f'{self.name}: checking response')
        self._check_response_on_errors(response)

        logger.debug(f'{self.name}: Converting response')
        return self.convert_response('translate', response)

    async def get_languages(self,
                            language: str,
                            model: str = 'nmt') -> t.List[str]:
        """
        reference: https://cloud.google.com/translate/docs/reference/languages
        """
        logger.debug('In get_languages')

        logger.debug('Making url and params')
        url = f'{self.endpoint}/languages'
        params = [
            ('target', language),
            ('model', model),
            ]

        logger.debug(f'{self.name}: Sending response')
        response = await self._send_request(url, params)

        logger.debug(f'{self.name}: checking response')
        self._check_response_on_errors(response)

        logger.debug(f'{self.name}: Converting response')
        return self.convert_response('translate', response)

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
