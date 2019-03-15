from environs import Env

from translate_wrapper.yandex import YandexEngine

env = Env()
env.read_env()
ENDPOINT_API = "https://translate.yandex.net/api/v1.5/tr.json"
endpoint = env.str("YANDEX_ENDPOIT", ENDPOINT_API)
engine = YandexEngine(api_key=env.str("YANDEX_API_KEY"), api_endpoint=endpoint)


async def test_get_langs():
    r = await engine.get_langs("ru")
    assert "dirs" in r.body
    assert "langs" in r.body


async def test_translate():
    response = await engine.translate("Hello, World!", "en-ru")
    assert response.status == 200
