import logging
import os
import typing as t
import uuid

import aiohttp

from translate_wrapper.exceptions import TranslationServiceError

from .engine import BaseEngine

logger = logging.getLogger('BingEngine')


class BingEngine(BaseEngine):
    """
    Implementation of Microsoft Translator API
    https://www.microsoft.com/en-us/translator/business/

    All documentations are here: https://docs.microsoft.com/ru-ru/azure/cognitive-services/translator/
    API reference: https://docs.microsoft.com/ru-ru/azure/cognitive-services/translator/reference/v3-0-reference

    NOTE: Each request is limited to 5,000 character. You're charged per character, not by the number of requests
    It's recommended to send shorter requests, and to have some requests outstanding at any given time.

    The Translator Text API has a maximum latency of 15 seconds using standard models
    By this time you'll have received a result or a timeout response.
    Typically, responses are returned in 150 milliseconds to 300 milliseconds
    """
    name = 'Bing'

    def __init__(self,
                 api_key: str,
                 api_endpoint: t.Optional[str] = None,
                 api_v: t.Optional[str] = None,
                 *,
                 event_loop=None):
        logger.debug(f'Creating {self.name} Engine with api key {api_key}')
        self.api_key = api_key
        self.endpoint = api_endpoint or os.getenv('BING_API_ENDPOINT')
        self.api_v = api_v or os.getenv('BING_API_V')

        self.event_loop = event_loop

    async def _send_request(self,
                            method: str,
                            url: str,
                            params: t.Optional[t.Dict[str, str]] = None,
                            body: t.Optional[t.List[t.Dict[str, str]]] = {}) -> t.Dict:

        logger.debug('In _send_request')
        async with aiohttp.ClientSession(loop=self.event_loop) as session:
            headers = {
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': self.api_key,
                'X-ClientTraceID': str(uuid.uuid4())
            }

            if not params:
                params = {}
            params['api-version'] = self.api_v

            logger.debug(f'Sending request to {self.name}')
            async with session.request(
                method=method,
                url=url,
                params=params,
                json=body,
                headers=headers
            ) as response:

                logger.debug('Retrieving json body from response')
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
        logger.debug('In translate')

        logger.debug('Making url and params')
        url = f'{self.endpoint}/translate'
        params = {
            'to': target,
            'textType': 'html',
        }

        if source:
            logger.debug('Appending source language')
            params['from'] = source

        body = []
        logger.debug('Appending each given line of the text to a query')
        for line in text:
            body.append({'Text': line})

        logger.debug(f'{self.name}: Sending request')
        response = await self._send_request('post', url, params, body)

        logger.debug(f'{self.name}: Checking response')
        self._check_response_on_errors(response)

        logger.debug(f'{self.name}: Converting response')
        return self.convert_response('translate', response)

    async def get_languages(self, *ignore) -> t.List[str]:
        """
        reference:
        https://docs.microsoft.com/ru-ru/azure/cognitive-services/translator/reference/v3-0-languages?tabs=curl
        """
        logger.debug('In get_languages')
        url = f'{self.endpoint}/languages'

        logger.debug(f'{self.name}: Sending request')
        response = await self._send_request('get', url)

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
        result = list(response['translation'].keys())
        return result

    @staticmethod
    def _convert_translate(response: t.Dict) -> t.List[str]:
        logger.debug('In _convert_translate')
        result = [item['translations'][0]['text'] for item in response]
        return result

    @staticmethod
    def _check_response_on_errors(response: t.Dict):
        logger.debug('In _check_response_on_error')
        if 'error' in response:
            raise TranslationServiceError('Bing', response['error']['code'], response['error']['message'])
