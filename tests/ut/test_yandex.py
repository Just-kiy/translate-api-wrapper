import pytest

from translate_wrapper.yandex import YandexEngine

pytestmark = [
    pytest.mark.ut,
    pytest.mark.engines,
    pytest.mark.yandex,
]


@pytest.fixture
def yandex_engine(event_loop):
    return YandexEngine(
        'api_key',
        'http://yandex-server.test',
        event_loop=event_loop
    )


class YandexEngineTest:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize('ui', [
        'ru', 'en', 'fr'
    ])
    async def test_get_langs(self, mocked_send_request, yandex_engine, ui):
        yandex_engine._send_request = mocked_send_request
        assert await yandex_engine.get_langs(ui)
        expected = {
            'url': f'{yandex_engine.endpoint}/getLangs',
            'params': {
                'ui': ui,
            }
        }
        mocked_send_request.assert_called_once_with(expected['url'], expected['params'])

    @pytest.mark.parametrize('text, lang, format', [
        ('Hello', 'ru', 'plain'),
        ('Darkness', 'fr', 'plain'),
        ('My old good friend', 'de', 'html'),
    ])
    async def test_translate(self, mocked_send_request, yandex_engine, text, lang, format):
        yandex_engine._send_request = mocked_send_request
        assert await yandex_engine.translate(text, lang, format)
        expected = {
            'url': f'{yandex_engine.endpoint}/translate',
            'params': {
                'lang': lang,
                'format': format,
            },
            'body': {
                'text': text
            },
        }
        mocked_send_request.assert_called_once_with(expected['url'], expected['params'], expected['body'])
