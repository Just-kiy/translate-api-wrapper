import pytest

import os

from environs import Env

from translate_wrapper.yandex import YandexEngine

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.e2e,
    pytest.mark.yandex,
    pytest.mark.engines,
    ]


@pytest.fixture
def yandex_engine(event_loop):
    env = Env()
    env.read_env()
    endpoint_api = 'https://translate.yandex.net/api/v1.5/tr.json'
    endpoint = env.str('YANDEX_ENDPOINT', endpoint_api)
    return YandexEngine(api_key=env.str('YANDEX_API_KEY'), api_endpoint=endpoint, event_loop=event_loop)


@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_get_langs(yandex_engine):
    response = await yandex_engine.get_langs('ru')
    assert 'en-ru' in response

@pytest.mark.skipif(not os.getenv('TESTING_E2E'), reason='expensive tests')
async def test_translate(yandex_engine):
    response = await yandex_engine.translate(text='Hello, World!', source='en', target='ru')
    assert len(response) == 1
    assert response[0].lower() == 'привет, мир!'
