import pytest
from environs import Env

import json
from translate_wrapper.google import GoogleEngine

env = Env()
env.read_env()
engine = GoogleEngine(api_key=env.str("GOOGLE_API_KEY"))

async def test_get_langs():
    r = await engine.get_langs("ru")
    assert r.status == 200
    assert "languages" in r.body

async def test_translate():
    response = await engine.translate(text="Hello, World!", target="ru")
    expected = "Привет, мир!"
    assert response.status == 200
    assert "translations" in response.body
    assert 'en' == response.body["translations"][0]["detectedSourceLanguage"]
    assert expected == response.body["translations"][0]["translatedText"]