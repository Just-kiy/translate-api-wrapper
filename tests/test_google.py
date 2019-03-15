from environs import Env

from translate_wrapper.google import GoogleEngine

env = Env()
env.read_env()
ENDPOINT_API = "https://translation.googleapis.com/language/translate/v2"
endpoint = env.str("GOOGLE_ENDPOINT", ENDPOINT_API)
engine = GoogleEngine(api_key=env.str("GOOGLE_API_KEY"), api_endpoint=endpoint)


async def test_get_langs():
    r = await engine.get_langs("ru")
    assert r.status == 200
    assert "languages" in r.body


async def test_translate():
    response = await engine.translate(text="Hello, World!", target="ru")
    assert response.status == 200
    assert "translations" in response.body
