import pytest

from .conftest import parse_response

from translate_wrapper.google import GoogleEngine

pytestmark = [
    pytest.mark.acceptance,
    pytest.mark.engines,
    pytest.mark.google,
]

# SIMPLE TEST CASE EXAMPLE


@pytest.fixture
def google_engine(event_loop, unused_tcp_port):
    return GoogleEngine(
        'api_key',
        f'http://127.0.0.1:{unused_tcp_port}',
        event_loop=event_loop
    )


# noinspection PyMethodMayBeStatic
class GoogleEngineTest:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize('target, model', [
        ('ru', 'nmt'),
        ('ru', 'base'),
        ('en', 'nmt'),
        ('en', 'base'),
    ])
    async def test_get_langs(self, unused_tcp_port, google_engine: 'GoogleEngine',
                             target, model):
        # NOTE: the testing echo server returns JSON Response
        # with only one key "echo" and reflected value
        response = await google_engine.get_langs(target, model)

        query = '&'.join((
            f'target={target}',
            f'model={model}',
            'key=api_key'
        ))

        result = parse_response(response['echo'])

        assert result['Method'] == 'POST'
        assert result['URL'] == f'/languages?{query}'
        assert result['Host'] == f'127.0.0.1:{unused_tcp_port}'
        assert result['User-Agent'] == 'Python/3.7 aiohttp/3.5.4'
        assert result['Content-Type'] == 'application/octet-stream'

    @pytest.mark.parametrize('text, target, source', [
        ('Hello', 'ru', 'en'),
        ('Hello', 'de', None),
        ('Hello', 'fr', 'en'),
        ('Hello', 'it', None),
    ])
    async def test_translate(self, unused_tcp_port, google_engine: 'GoogleEngine',
                             text, target, source):
        response = await google_engine.translate(text, target, source)

        q = f'q={text}'
        _target = f'target={target}'
        _source = f'source={source}' if source else ''
        key = f'key=api_key'

        query = '&'.join((q, _target, _source, key))

        result = parse_response(response['echo'])

        assert result['Method'] == 'POST'
        assert result['URL'] == f'/languages?{query}'
        assert result['Host'] == f'127.0.0.1:{unused_tcp_port}'
        assert result['User-Agent'] == 'Python/3.7 aiohttp/3.5.4'
        assert result['Content-Type'] == 'application/json'
