import pytest

from translate_wrapper.engines.bing import BingEngine
from translate_wrapper.engines.google import GoogleEngine
from translate_wrapper.engines.yandex import YandexEngine
from translate_wrapper.translators import Translator, translate_engines


@pytest.fixture
def engines():
    _engines = translate_engines
    _engines.register(translator_name='yandex', engine=YandexEngine)
    _engines.register(translator_name='google', engine=GoogleEngine)
    _engines.register(translator_name='bing', engine=BingEngine)
    return _engines


class TranslatorTest:
    @pytest.mark.parametrize('translator_name, engine', [
        ('yandex', YandexEngine),
        ('google', GoogleEngine),
        ('bing', BingEngine),
    ])
    def test_get_translator(self, engines, translator_name, engine):
        translator = Translator.get_translator(translator_name=translator_name, api_key='some_api_key')
        isinstance(translator._engine, engine)
