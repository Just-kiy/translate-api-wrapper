import pytest

import os

from environs import Env

from translate_wrapper.google import GoogleEngine

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.e2e,
    pytest.mark.google,
    pytest.mark.engines,
    ]


@pytest.fixture
def google_engine(event_loop):
    env = Env()
    env.read_env()
    endpoint_api = 'https://translation.googleapis.com/language/translate/v2'
    endpoint = env.str('GOOGLE_ENDPOINT', endpoint_api)
    return GoogleEngine(api_key=env.str('GOOGLE_API_KEY'), api_endpoint=endpoint, event_loop=event_loop)


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_get_langs(google_engine):
    response = await google_engine.get_langs('ru')
    assert 'data' in response
    assert 'languages' in response['data']


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_translate(google_engine):
    response = await google_engine.translate(text='Hello, World!', target='ru')
    assert 'data' in response
    assert 'translations' in response['data']
    assert 'en' == response['data']['translations'][0]['detectedSourceLanguage']
