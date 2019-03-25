import pytest
import json
import requests

from translate_wrapper.bing import BingEngine

pytestmark = [
    pytest.mark.acceptance,
    pytest.mark.engines,
    pytest.mark.bing,
]

# SIMPLE TEST CASE EXAMPLE


@pytest.fixture
def bing_engine(event_loop, unused_tcp_port):
    return BingEngine(
        'api_key',
        f'http://127.0.0.1:{unused_tcp_port}',
        'v1',
        event_loop=event_loop
    )


# noinspection PyMethodMayBeStatic
class BingEngineTest:
    pytestmark = pytest.mark.asyncio

    async def test_bla(self, unused_tcp_port, bing_engine: 'BingEngine'):
        # NOTE: the testing echo server returns JSON Response
        # with only one key "echo" and reflected value
        result = await bing_engine.get_langs()

        assert result['echo'] == (
            'GET /languages?api-version=v1 HTTP/1.1\r\n'
            f'Host: 127.0.0.1:{unused_tcp_port}\r\n'
            'Content-Type: application/json\r\n'
            'Ocp-Apim-Subscription-Key: api_key\r\n'
            'Accept: */*\r\nAccept-Encoding: gzip, deflate\r\n'
            'User-Agent: Python/3.7 aiohttp/3.5.4\r\n\r\n'
        )
