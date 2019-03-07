import pytest
from environs import Env

import json
from translate_wrapper.yandex import YandexEngine

env = Env()
env.read_env()
engine = YandexEngine(api_key=env.str("YANDEX_API_KEY"))

async def test_get_langs():
    r = await engine.get_langs("ru")
    assert "dirs" in r.body
    assert "langs" in r.body

async def test_translate():
    response = await engine.translate("Hello, World!", "en-ru")
    expected = "Привет, Мир!"
    assert response.status == 200
    assert expected in response.body['text']
