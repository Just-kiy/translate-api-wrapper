import pytest

import typing as t

from translate_wrapper.bing import BingEngine
from translate_wrapper.engine import BaseEngine
from translate_wrapper.google import GoogleEngine
from translate_wrapper.translators import TranslatorFactory
from translate_wrapper.yandex import YandexEngine

pytestmark = [
    pytest.mark.ut,
    pytest.mark.engines,
    pytest.mark.translator,
]

engines = [
    {
        'name': 'yandex',
        'implementation': YandexEngine
    },
    {
        'name': 'bing',
        'implementation': BingEngine
    },
    {
        'name': 'google',
        'implementation': GoogleEngine
    },
]


@pytest.fixture
def factory():
    return TranslatorFactory()


class TranslatorTest:
    @pytest.mark.parametrize('engine', engines)
    def test_register_engine(self, engine, factory):
        factory.register_engine(**engine)
        assert engine['name'] in factory._engines

    @pytest.mark.parametrize('engine', engines)
    def test_get_translator(self, engine, factory):
        factory.register_engine(**engine)
        translator = factory.get_translator(engine['name'])
        assert issubclass(translator, BaseEngine)
