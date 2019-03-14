from environs import Env

from translate_wrapper.bing import BingEngine

env = Env()
env.read_env()
engine = BingEngine(api_key=env.str("BING_API_KEY"))


async def test_get_langs():
    r = await engine.get_langs("ru")
    assert r.status == 200
    assert "translation" in r.body


async def test_translate():
    response = await engine.translate(text="Hello, World!", target="ru")
    assert response.status == 200
    assert "translations" in response.body[0]
