import pytest

import os

from environs import Env

from translate_wrapper.yandex import YandexEngine

@pytest.fixture
def yandex_engine():
    env = Env()
    env.read_env()
    ENDPOINT_API = "https://translate.yandex.net/api/v1.5/tr.json"
    endpoint = env.str("YANDEX_ENDPOIT", ENDPOINT_API)
    return YandexEngine(api_key=env.str("YANDEX_API_KEY"), api_endpoint=endpoint)


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_get_langs(yandex_engine):
    r = await yandex_engine.get_langs("ru")
    assert "dirs" in r.body
    assert "langs" in r.body


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_translate(yandex_engine):
    response = await yandex_engine.translate("Hello, World!", "en-ru")
    assert response.status == 200
