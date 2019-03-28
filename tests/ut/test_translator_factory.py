import pytest

from translate_wrapper.bing import BingEngine
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
        'implementation': YandexEngine,
        'config': {
            'api_key': 'API_KEY',
            'api_endpoint': 'API_ENDPOINT',
            'event_loop': None,
        }
    },
    {
        'name': 'google',
        'implementation': GoogleEngine,
        'config': {
            'api_key': 'API_KEY',
            'api_endpoint': 'API_ENDPOINT',
            'event_loop': None,
        },
    },
    {
        'name': 'bing',
        'implementation': BingEngine,
        'config': {
            'api_key': 'API_KEY',
            'api_endpoint': 'API_ENDPOINT',
            'api_v': 'API_V',
            'event_loop': None,
        },
    },
]


@pytest.fixture
def factory():
    return TranslatorFactory()


class TranslatorTest:
    @pytest.mark.parametrize('engine', engines)
    def test_register_translator(self, engine, factory):
        factory.register_translator(**engine)
        assert engine['name'] in factory._translators

    @pytest.mark.parametrize('engine', engines)
    def test_get_translator(self, engine, factory):
        factory.register_translator(**engine)
        translator = factory.get_translator(engine['name'])
        assert isinstance(translator._engine, engine['implementation'])
