import logging
import os
import typing as t

import aiohttp

from translate_wrapper.exceptions import TranslationServiceError

from .engine import BaseEngine

logger = logging.getLogger('YandexEngine')


class YandexEngine(BaseEngine):
    """
    Implementation of Yandex.Translate
    https://tech.yandex.ru/translate/

    All documentations are here: https://tech.yandex.ru/translate/doc/dg/concepts/about-docpage/

    POST-requests are limited by 10 000 characters
    GET-requests are limited only by query string, from 2 to 10 kbs (depending on browser)

    """
    name = 'Yandex'

    def __init__(self,
                 api_key: str,
                 api_endpoint: t.Optional[str] = None,
                 *,
                 event_loop=None,
                 sesion=None):
        logger.debug(f'Creating {self.name} Engine with api key {api_key}')
        self.api_key = api_key
        self.endpoint = api_endpoint or os.getenv('YANDEX_API_ENDPOINT')
        self.event_loop = event_loop
        self.session = sesion
        self.error_codes = [401, 402, 404, 413, 422, 501]

    async def release(self):
        await self.session.close()

    async def _send_request(self,
                            url: str,
                            params: t.Dict[str, str],
                            body: t.Optional[t.Dict[str, str]] = None) -> t.Dict:

        logger.debug('In _send_request')

        params['key'] = self.api_key

        logger.debug(f'Sending request to {self.name}')
        async with self.session.post(url, params=params, data=body) as response:

            logger.debug('Retrieving json body from response')
            body = await response.json()
            return body

    async def translate(self,
                        *text: str,
                        target: str,
                        source: t.Optional[str]) -> t.List:
        """
        reference: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
        """
        logger.debug('In translate')

        logger.debug('Making url and params')
        url = f'{self.endpoint}/translate'
        lang = target

        if source:
            logger.debug('Appending source language')
            lang = f'{source}-{target}'

        params = {
            'lang': lang,
            'format': 'html',
        }

        logger.debug('Appending each given line of the text to a query')
        body = []
        for line in text:
            body.append(('text', line))

        logger.debug(f'{self.name}: Sending request')
        response = await self._send_request(url, params, body)

        logger.debug(f'{self.name}: Checking response')
        self._check_response_on_errors(response)

        logger.debug(f'{self.name}: Converting response')
        return self.convert_response('translate', response)

    async def get_languages(self, lang: str) -> t.List:
        """
        reference: https://tech.yandex.ru/translate/doc/dg/reference/getLangs-docpage/
        """
        logger.debug('In get_languages')

        logger.debug('Making url and params')
        url = f'{self.endpoint}/getLangs'
        params = {
            'ui': lang
        }

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
        result = list(response['langs'].keys())
        return result

    @staticmethod
    def _convert_translate(response: t.Dict) -> t.List[str]:
        logger.debug('In _convert_translate')
        result = response['text']
        return result

    def _check_response_on_errors(self, response: t.Dict):
        logger.debug('In _check_response_on_error')
        if 'code' in response and response['code'] in self.error_codes:
            raise TranslationServiceError('Yandex', response['code'], response['message'])
