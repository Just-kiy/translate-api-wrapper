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
            'url': 'http://yandex-server.test/getLangs',
            'params': {
                'ui': ui,
            }
        }

        mocked_send_request.assert_called_once_with(expected['url'], expected['params'])
