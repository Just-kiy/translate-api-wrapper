import pytest

import urllib.parse

from translate_wrapper.yandex import YandexEngine

from .conftest import parse_response

pytestmark = [
    pytest.mark.acceptance,
    pytest.mark.engines,
    pytest.mark.yandex,
]

# SIMPLE TEST CASE EXAMPLE


@pytest.fixture
def yandex_engine(event_loop, unused_tcp_port):
    return YandexEngine(
        'api_key',
        f'http://127.0.0.1:{unused_tcp_port}',
        event_loop=event_loop
    )


# noinspection PyMethodMayBeStatic
class YandexEngineTest:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize('ui', [
        'ru', 'en', 'fr'
    ])
    async def test_get_langs(self, unused_tcp_port, yandex_engine: 'YandexEngine', ui):
        response = await yandex_engine.get_langs(ui)

        params = {
            'ui': [ui],
            'key': ['api_key']
        }

        result = parse_response(response['echo'])
        q_result = urllib.parse.urlparse(result['URL'])

        assert result['Method'] == 'POST'
        assert urllib.parse.parse_qs(q_result[4]) == params
        assert result['Host'] == f'127.0.0.1:{unused_tcp_port}'
        assert result['User-Agent'] == 'Python/3.7 aiohttp/3.5.4'
        assert result['Content-Type'] == 'application/octet-stream'

    @pytest.mark.parametrize('text, lang', [
        ('Hello', 'ru'),
        ('Darkness', 'fr'),
        ('My old good friend', 'de'),
    ])
    async def test_translate(self, unused_tcp_port, yandex_engine: 'YandexEngine', text, lang):
        response = await yandex_engine.translate(text, lang)

        params = {
            'lang': [lang],
            'key': ['api_key']
        }

        result = parse_response(response['echo'])
        q_result = urllib.parse.urlparse(result['URL'])

        assert result['Method'] == 'POST'
        assert urllib.parse.parse_qs(q_result[4]) == params
        assert result['Host'] == f'127.0.0.1:{unused_tcp_port}'
        assert result['User-Agent'] == 'Python/3.7 aiohttp/3.5.4'
        assert result['Content-Type'] == 'application/x-www-form-urlencoded'
