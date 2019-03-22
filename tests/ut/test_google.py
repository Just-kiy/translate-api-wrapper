import pytest

from translate_wrapper.google import GoogleEngine

pytestmark = [
    pytest.mark.ut,
    pytest.mark.engines,
    pytest.mark.google,
]


@pytest.fixture
def google_engine(event_loop):
    return GoogleEngine(
        'api_key',
        'http://google-server.test',
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
    async def test_get_langs(self, mocked_send_request, google_engine, target, model):
        google_engine._send_request = mocked_send_request
        assert await google_engine.get_langs(target, model)
        expected = {
            'url': f'{google_engine.endpoint}/languages',
            'params': {
                'target': target,
                'model': model,
            }
        }
        mocked_send_request.assert_called_once_with(expected['url'], expected['params'])

    @pytest.mark.parametrize('text, target, source, model', [
        ('Hello', 'ru', 'en', 'nmt'),
        ('Hello', 'de', None, 'base'),
        ('Hello', 'fr', 'en', None),
        ('Hello', 'it', None, 'qwe'),
    ])
    async def test_translate(self, mocked_send_request, google_engine, text, target, source, model):
        google_engine._send_request = mocked_send_request
        assert await google_engine.translate(text, target, source, model)
        expected = {
            'url': google_engine.endpoint,
            'params': {
                'q': text,
                'target': target,
                'model': model,
            }
        }
        if source:
            expected['params']['source'] = source
        if model not in ('base', 'nmt'):
            expected['params']['model'] = 'nmt'

        mocked_send_request.assert_called_once_with(expected['url'], expected['params'])
