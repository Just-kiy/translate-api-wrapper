import typing as t

import aiohttp

from .engine import BaseEngine, BaseResponseConverter


class BingEngine(BaseEngine):
    def __init__(self,
                 api_key: str,
                 api_endpoint: str,
                 api_v: str,
                 *,
                 event_loop=None):
        self.api_key = api_key
        self.endpoint = api_endpoint
        self.api_v = api_v

        self.event_loop = event_loop

    async def _send_request(self,
                            method: str,
                            url: str,
                            params: t.Optional[t.Dict[str, str]] = None,
                            body: t.Optional[t.List[t.Dict[str, str]]] = None):
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
                        source: t.Optional[str] = None) -> t.List[t.Dict]:
        url = f'{self.endpoint}/translate'
        params = {
            'to': target,
        }
        if source:
            params['from'] = source
        body = [{'Text': text}]
        return await self._send_request('post', url, params, body)

    async def get_langs(self) -> t.List[t.Dict]:
        url = f'{self.endpoint}/languages'
        return await self._send_request('get', url)

    def convert_response(self, response: t.Dict) -> t.Dict:
        '''
        Convert response from Bing representation to Base Schema
        :param (Dict) response: pure json containing info from server
        :return: (Dict) Base Schema Dict
        '''
        return response


class BingResponse(BaseResponseConverter):
    def __init__(self, response, body):
        super().__init__(response)
        self.body = body

