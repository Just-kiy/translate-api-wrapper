import asyncio

import pytest

from translate_wrapper.google import GoogleEngine

pytestmark = [
    pytest.mark.ut,
    pytest.mark.engines,
    pytest.mark.google,
]


@pytest.fixture
def google_engine():
    return GoogleEngine(
        'api_key',
        'http://google-server.test',
        event_loop='event_loop'
    )


class GoogleEngineTest:
    async def test_get_langs(self, mocker, google_engine):
        mocked_result = asyncio.Future()
        mocked_result.set_result(True)

        mocked_send_request = mocker.Mock(return_value=mocked_result)
        google_engine._send_request = mocked_send_request

        assert await google_engine.get_langs('ru')

        mocked_send_request.assert_called_once_with('get', 'http://google-server.test/languages')
