import pytest

import os

from environs import Env

from translate_wrapper.bing import BingEngine

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.e2e,
    pytest.mark.bing,
    pytest.mark.engines,
    ]


@pytest.fixture
def bing_engine(event_loop):
    env = Env()
    env.read_env()
    endpoint_api = 'https://api.cognitive.microsofttranslator.com'
    api_version = '3.0'
    endpoint = env.str('BING_ENDPOINT', endpoint_api)
    api_v = env.str('BING_API_V', api_version)
    return BingEngine(api_key=env.str('BING_API_KEY'), api_endpoint=endpoint, api_v=api_v, event_loop=event_loop)


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_get_langs(bing_engine):
    response = await bing_engine.get_languages()
    assert 'en' in response


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_translate(bing_engine):
    response = await bing_engine.translate(text='Hello!', target='ru')
    assert len(response) == 1
    assert response[0].lower() == 'привет!'
