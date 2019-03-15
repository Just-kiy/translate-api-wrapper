from environs import Env

from translate_wrapper.bing import BingEngine

ENDPOINT_API = "https://api.cognitive.microsofttranslator.com"
API_V = "3.0"

env = Env()
env.read_env()
endpoint = env.str("BING_ENDPOINT", ENDPOINT_API)
api_v = env.str("BING_API_V", API_V)
engine = BingEngine(api_key=env.str("BING_API_KEY"), api_endpoint=endpoint, api_v=api_v)


async def test_get_langs():
    r = await engine.get_langs("ru")
    assert r.status == 200
    assert "translation" in r.body


async def test_translate():
    response = await engine.translate(text="Hello, World!", target="ru")
    assert response.status == 200
    assert "translations" in response.body[0]
