import pytest

from .conftest import parse_response

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

    async def test_get_langs(self, unused_tcp_port, bing_engine: 'BingEngine'):
        response = await bing_engine.get_langs()

        result = parse_response(response['echo'])

        assert result['Method'] == 'GET'
        assert result['URL'] == '/languages?api-version=v1'
        assert result['Host'] == f'127.0.0.1:{unused_tcp_port}'
        assert result['User-Agent'] == 'Python/3.7 aiohttp/3.5.4'
        assert result['Content-Type'] == 'application/json'
        assert result['Ocp-Apim-Subscription-Key'] == 'api_key'

    @pytest.mark.parametrize('text, target, source', [
        ('One', 'ru', 'en'),
        ('Two', 'de', None),
        ('Three', 'fr', 'en'),
        ('Four', 'it', None),
    ])
    async def test_translate(self, unused_tcp_port, bing_engine: 'BingEngine',
                             text, target, source):
        response = await bing_engine.translate(text, target, source)

        content = [{'Text': text}]
        to = f'to={target}'
        _from = f'from={source}' if source else None
        api_v = 'api-version=v1'
        query = '&'.join((to, _from)) if _from else to

        result = parse_response(response['echo'])

        print(result)

        assert result['Method'] == 'POST'
        assert result['URL'] == f'/translate?{query}&{api_v}'
        assert result['Host'] == f'127.0.0.1:{unused_tcp_port}'
        assert result['Content-Type'] == 'application/json'
        assert result['Ocp-Apim-Subscription-Key'] == 'api_key'
        assert result['User-Agent'] == 'Python/3.7 aiohttp/3.5.4'
        assert result['Content-Length'] == f'{len(content.__str__())}'
