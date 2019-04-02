import asyncio
import pytest

from translate_wrapper.bing import BingEngine

pytestmark = [
    pytest.mark.ut,
    pytest.mark.engines,
    pytest.mark.bing,
]

ENDPOINT = 'http://bing-server.test'


def mock_send_request(mocker):
    mocker_response = {
        'translation': {
            'en': {
                'name': 'English',
                'nativeName': 'English',
                'dir': 'ltr'
            },
        },
        'translate': {
            'detectedLanguage': {
                'language': 'en',
                'score': 1.0
            },
            'translations': [
                {
                    'text': 'Еще один Привет',
                    'to': 'ru'
                }
            ]
        }
    }
    mocked_result = asyncio.Future()
    mocked_result.set_result(mocker_response)
    mocked_send_request = mocker.Mock(return_value=mocked_result)
    return mocked_send_request


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

    async def test_get_langs(self, mocker, bing_engine):
        mocked_send_request = mock_send_request(mocker)
        mocked_convert_response = mocker.Mock(return_value='en')

        bing_engine._send_request = mocked_send_request
        bing_engine.convert_response = mocked_convert_response

        assert await bing_engine.get_languages()

        expected = {
            'method': 'get',
            'url': ENDPOINT + '/languages',
        }

        mocked_send_request.assert_called_once_with(expected['method'], expected['url'])
        mocked_convert_response.assert_called_once()

    @pytest.mark.parametrize('text, target, source', [
        ('Hello', 'ru', 'en'),
        ('Hello', 'de', None),
        ('Hello', 'fr', 'en'),
        ('Hello', 'it', None),
    ])
    async def test_translate(self, mocker, bing_engine, text, target, source):
        mocked_send_request = mock_send_request(mocker)
        mocked_convert_response = mocker.Mock(return_value='en')

        bing_engine._send_request = mocked_send_request
        bing_engine.convert_response = mocked_convert_response

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
        mocked_convert_response.assert_called_once()
