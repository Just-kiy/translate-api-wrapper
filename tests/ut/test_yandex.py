import pytest

from translate_wrapper.yandex import YandexEngine

pytestmark = [
    pytest.mark.ut,
    pytest.mark.engines,
    pytest.mark.yandex,
]

ENDPOINT = 'http://yandex-server.test'


@pytest.fixture
def yandex_engine(event_loop):
    return YandexEngine(
        'api_key',
        ENDPOINT,
        event_loop=event_loop
    )


class YandexEngineTest:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize('ui', [
        'ru', 'en', 'fr'
    ])
    async def test_get_langs(self, mocked_send_request, yandex_engine, ui):
        yandex_engine._send_request = mocked_send_request
        assert await yandex_engine.get_languages(ui)
        expected = {
            'url': ENDPOINT + '/getLangs',
            'params': {
                'ui': ui,
            }
        }
        mocked_send_request.assert_called_once_with(expected['url'], expected['params'])

    @pytest.mark.skip
    @pytest.mark.parametrize('text, target, source', [
        ('Hello', 'ru', 'en'),
        ('Darkness', 'fr', 'en'),
        ('мой старый давний друг', 'en', 'ru'),
    ])
    async def test_translate(self, mocked_send_request, yandex_engine, text, target, source):
        yandex_engine._send_request = mocked_send_request
        assert await yandex_engine.translate(source=source, target=target, text=text)
        expected = {
            'url': ENDPOINT + '/translate',
            'params': {
                'lang': f'{source}+{target}',
            },
            'body': {
                'text': text
            },
        }
        mocked_send_request.assert_called_once_with(expected['url'], expected['params'], expected['body'])
