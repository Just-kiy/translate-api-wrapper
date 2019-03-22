import asyncio

import pytest

from translate_wrapper.bing import BingEngine

pytestmark = [
    pytest.mark.ut,

    pytest.mark.engines,
    pytest.mark.bing,
]


@pytest.fixture
def bing_engine():
    return BingEngine(
        'api_key',
        'http://bing-server.test',
        'v1',
        event_loop='event_loop'
    )


class BingEngineTest:
    async def test_get_langs(self, mocker, bing_engine):
        mocked_result = asyncio.Future()
        mocked_result.set_result(True)

        mocked_send_request = mocker.Mock(return_value=mocked_result)
        bing_engine._send_request = mocked_send_request

        assert await bing_engine.get_langs()

        mocked_send_request.assert_called_once_with('get', 'http://bing-server.test/languages')
