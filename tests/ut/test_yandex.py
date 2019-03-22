import asyncio

import pytest

from translate_wrapper.yandex import YandexEngine

pytestmark = [
    pytest.mark.ut,
    pytest.mark.engines,
    pytest.mark.yandex,
]


@pytest.fixture
def yandex_engine():
    return YandexEngine(
        'api_key',
        'http://yandex-server.test',
        event_loop='event_loop'
    )


class YandexEngineTest:
    async def test_get_langs(self, mocker, yandex_engine):
        mocked_result = asyncio.Future()
        mocked_result.set_result(True)

        mocked_send_request = mocker.Mock(return_value=mocked_result)
        yandex_engine._send_request = mocked_send_request

        assert await yandex_engine.get_langs('ru')

        mocked_send_request.assert_called_once_with('get', 'http://yandex-server.test/languages?api_key=api_key?lang=ru')
