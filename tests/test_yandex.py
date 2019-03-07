import pytest

import json
from translate_wrapper.yandex import YandexEngine

API_KEY="trnsl.1.1.20190221T131631Z.1acbec869a7303cf.9b1b624de49bf0b1bd8bf754f0ba6a418881a90f"
engine = YandexEngine(api_key=API_KEY)

async def test_get_langs():
    r = await engine.get_langs("ru")
    assert "dirs" in r.body
    assert "langs" in r.body

async def test_translate():
    response = await engine.translate("Hello, World!", "en-ru")
    expected = "Привет, Мир!"
    assert response.status == 200
    assert expected in response.body['text']
