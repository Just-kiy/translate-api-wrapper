import asyncio
import pytest

from translate_wrapper.google import GoogleEngine

pytestmark = [
    pytest.mark.ut,
    pytest.mark.engines,
    pytest.mark.google,
]

ENDPOINT = 'http://google-server.test'


def mock_send_request(mocker):
    mocker_response = {
        'data': {
            'languages': [
                    {'language': 'en'}, {'language': 'ru'}
                ],
            "translations": [
              {
                "translatedText": "Привет",
                "model": "nmt"
              }
            ]
        }
    }
    mocked_result = asyncio.Future()
    mocked_result.set_result(mocker_response)
    mocked_send_request = mocker.Mock(return_value=mocked_result)
    return mocked_send_request


@pytest.fixture
def google_engine(event_loop):
    return GoogleEngine(
        'api_key',
        ENDPOINT,
        event_loop=event_loop
    )


class GoogleEngineTest:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize('target, model', [
        ('ru', 'nmt'),
        ('ru', 'base'),
        ('en', 'nmt'),
        ('en', 'base'),
    ])
    async def test_get_langs(self, mocker, google_engine, target, model):
        mocked_send_request = mock_send_request(mocker)
        mocked_convert_response = mocker.Mock(return_value='es')

        google_engine._send_request = mocked_send_request
        google_engine.convert_response = mocked_convert_response
        assert await google_engine.get_languages(target, model)
        expected = {
            'url': ENDPOINT + '/languages',
            'params': {
                'target': target,
                'model': model,
            }
        }
        mocked_send_request.assert_called_once_with(expected['url'], expected['params'])
        mocked_convert_response.assert_called_once()

    @pytest.mark.parametrize('text, target, source', [
        ('Hello', 'ru', 'en'),
        ('Hello', 'de', None),
        ('Hello', 'fr', 'en'),
        ('Hello', 'it', None),
    ])
    async def test_translate(self, mocker, google_engine, text, target, source):
        mocked_send_request = mock_send_request(mocker)
        mocked_convert_response = mocker.Mock(return_value='Привет')

        google_engine._send_request = mocked_send_request
        google_engine.convert_response = mocked_convert_response
        assert await google_engine.translate(text, target, source)
        expected = {
            'url': ENDPOINT,
            'params': {
                'q': text,
                'target': target,
            }
        }
        if source:
            expected['params']['source'] = source

        mocked_send_request.assert_called_once_with(expected['url'], expected['params'])
        mocked_convert_response.assert_called_once()
