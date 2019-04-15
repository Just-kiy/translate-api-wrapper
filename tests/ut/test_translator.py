import pytest

from translate_wrapper.engines.bing import BingEngine
from translate_wrapper.engines.google import GoogleEngine
from translate_wrapper.engines.yandex import YandexEngine
from translate_wrapper.translators import Translator, _TranslateEngines


@pytest.fixture
def engines():
    _engines = _TranslateEngines()
    _engines.register(engine=YandexEngine)
    _engines.register(engine=GoogleEngine)
    _engines.register(engine=BingEngine)
    return _engines


class TranslatorTest:
    @pytest.mark.asyncio
    @pytest.mark.parametrize('translator_name, engine', [
        ('Yandex', YandexEngine),
        ('Google', GoogleEngine),
        ('Bing', BingEngine),
    ])
    async def test_get_translator(self, engines, translator_name, engine):
        translator = await Translator.get_translator(translator_name=translator_name, api_key='some_api_key')
        isinstance(translator._engine, engine)
