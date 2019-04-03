import pytest

import asyncio

from translate_wrapper.engines.yandex import YandexEngine
from translate_wrapper.exceptions import EngineGetLangsError, EngineTranslationError

pytestmark = [
    pytest.mark.ut,
    pytest.mark.engines,
    pytest.mark.yandex,
]

ENDPOINT = 'http://yandex-server.test'


def mock_send_request(mocker):
    mocker_response = {
        'langs': {
            'es': 'Испанский'
        },
        'text': [
            'привет'
        ]
    }
    mocked_result = asyncio.Future()
    mocked_result.set_result(mocker_response)
    mocked_send_request = mocker.Mock(return_value=mocked_result)
    return mocked_send_request


@pytest.fixture
def yandex_engine(event_loop):
    return YandexEngine(
        'api_key',
        ENDPOINT,
        event_loop=event_loop
    )


class YandexEngineTest:
    @pytest.mark.asyncio
    @pytest.mark.parametrize('ui', [
        'ru', 'en', 'fr'
    ])
    async def test_get_langs(self, mocker, yandex_engine, ui):
        mocked_send_request = mock_send_request(mocker)
        mocked_convert_response = mocker.Mock(return_value='es')

        yandex_engine._send_request = mocked_send_request
        yandex_engine.convert_response = mocked_convert_response
        assert await yandex_engine.get_languages(ui)
        expected = {
            'url': ENDPOINT + '/getLangs',
            'params': {
                'ui': ui,
            }
        }
        mocked_send_request.assert_called_once_with(expected['url'], expected['params'])
        mocked_convert_response.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize('text, target, source', [
        ('Hello', 'ru', 'en'),
        ('Darkness', 'fr', 'en'),
        ('мой старый давний друг', 'en', 'ru'),
    ])
    async def test_translate(self, mocker, yandex_engine, text, target, source):
        mocked_send_request = mock_send_request(mocker)
        mocked_convert_response = mocker.Mock(return_value='Привет')

        yandex_engine._send_request = mocked_send_request
        yandex_engine.convert_response = mocked_convert_response
        assert await yandex_engine.translate(source=source, target=target, text=text)
        expected = {
            'url': ENDPOINT + '/translate',
            'params': {
                'lang': f'{source}-{target}',
            },
            'body': {
                'text': text
            },
        }
        mocked_send_request.assert_called_once_with(expected['url'], expected['params'], expected['body'])
        mocked_convert_response.assert_called_once()

    def test_convert_response_get_langs(self, yandex_engine):
        response_from_server = {'langs': {
                'en': 'Английски',
                'es': 'Испанский',
                'ru': 'Русский',
            }
        }
        result = yandex_engine.convert_response('get_langs', response_from_server)
        assert result == ['en', 'es', 'ru']

    def test_convert_response_get_langs_error(self, yandex_engine):
        response_from_server = {
            'code': 401,
            'message': 'API key is invalid'
        }
        with pytest.raises(EngineGetLangsError):
            yandex_engine.convert_response('get_langs', response_from_server)

    def test_convert_response_translate(self, yandex_engine):
        response_from_server = {
                'code': 200,
                'lang': 'en-ru',
                'text': [
                    'привет',
                    'мир'
                ]
            }
        result = yandex_engine.convert_response('translate', response_from_server)
        assert result == ['привет', 'мир']

    def test_convert_response_translate_error(self, yandex_engine):
        response_from_server = {
            'code': 501,
            'message': 'The specified translation direction is not supported'
        }
        with pytest.raises(EngineTranslationError):
            yandex_engine.convert_response('translate', response_from_server)
