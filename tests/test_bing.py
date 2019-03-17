import pytest

import os

from environs import Env

from translate_wrapper.bing import BingEngine

ENDPOINT_API = "https://api.cognitive.microsofttranslator.com"
API_V = "3.0"


@pytest.fixture
def bing_engine():
    # TODO: do not use global variables even if this is a test
    env = Env()
    env.read_env()
    endpoint = env.str("BING_ENDPOINT", ENDPOINT_API)
    api_v = env.str("BING_API_V", API_V)
    return BingEngine(api_key=env.str("BING_API_KEY"), api_endpoint=endpoint, api_v=api_v)


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_get_langs(bing_engine):
    r = await bing_engine.get_langs("ru")

    assert r.status == 200
    assert "translation" in r.body


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_translate(bing_engine):
    response = await bing_engine.translate(text="Hello, World!", target="ru")

    assert response.status == 200
    assert "translations" in response.body[0]
