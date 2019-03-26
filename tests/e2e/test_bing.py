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
    response = await bing_engine.get_langs()
    assert 'translation' in response
    assert 'transliteration' in response
    assert 'dictionary' in response


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_translate(bing_engine):
    response = await bing_engine.translate(text='Hello, World!', target='ru')
    assert 'translations' in response[0]
    assert 'ru' == response[0]['translations'][0]['to']
