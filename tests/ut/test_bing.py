import pytest

from translate_wrapper.bing import BingEngine

pytestmark = [
    pytest.mark.ut,
    pytest.mark.engines,
    pytest.mark.bing,
]


@pytest.fixture
def bing_engine(event_loop):
    return BingEngine(
        'api_key',
        'http://bing-server.test',
        'v1',
        event_loop=event_loop
    )


class BingEngineTest:
    pytestmark = pytest.mark.asyncio

    async def test_get_langs(self, mocked_send_request, bing_engine):
        bing_engine._send_request = mocked_send_request

        assert await bing_engine.get_langs()

        expected = {
            'method': 'get',
            'url': 'http://bing-server.test/languages',
        }

        mocked_send_request.assert_called_once_with(expected['method'], expected['url'])
