import pytest

import os

from environs import Env

from translate_wrapper.google import GoogleEngine

@pytest.fixture
def google_engine():
    env = Env()
    env.read_env()
    ENDPOINT_API = 'https://translation.googleapis.com/language/translate/v2'
    endpoint = env.str('GOOGLE_ENDPOINT', ENDPOINT_API)
    return GoogleEngine(api_key=env.str('GOOGLE_API_KEY'), api_endpoint=endpoint)


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_get_langs(google_engine):
    r = await google_engine.get_langs('ru')
    assert r.status == 200
    assert 'languages' in r.body


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_translate(google_engine):
    response = await google_engine.translate(text='Hello, World!', target='ru')    
    assert response.status == 200
    assert 'translations' in response.body
