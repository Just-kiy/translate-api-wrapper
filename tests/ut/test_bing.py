import pytest

from translate_wrapper.bing import BingEngine

pytestmark = [
    pytest.mark.ut,
    pytest.mark.engines,
    pytest.mark.bing,
]

ENDPOINT = 'http://bing-server.test'


@pytest.fixture
def bing_engine(event_loop):
    return BingEngine(
        'api_key',
        ENDPOINT,
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
            'url': ENDPOINT + '/languages',
        }

        mocked_send_request.assert_called_once_with(expected['method'], expected['url'])

    @pytest.mark.parametrize('text, target, source', [
        ('Hello', 'ru', 'en'),
        ('Hello', 'de', None),
        ('Hello', 'fr', 'en'),
        ('Hello', 'it', None),
    ])
    async def test_translate(self, mocked_send_request, bing_engine, text, target, source):
        bing_engine._send_request = mocked_send_request

        assert await bing_engine.translate(text, target, source)

        expected = {
            'method': 'post',
            'url': ENDPOINT + '/translate',
            'params': {
                'to': target,
            },
            'body': [
                {
                    'Text': text,
                }
            ]
        }
        if source:
            expected['params']['from'] = source

        mocked_send_request.assert_called_once_with(expected['method'], expected['url'],
                                                    expected['params'], expected['body'])
