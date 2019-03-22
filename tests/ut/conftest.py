import asyncio

import pytest


@pytest.fixture()
def mocked_send_request(mocker):
    mocked_result = asyncio.Future()
    mocked_result.set_result(True)

    mocked_send_request = mocker.Mock(return_value=mocked_result)
    return mocked_send_request
