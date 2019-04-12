__version__ = '1.0.0'

from .engines.bing import BingEngine
from .engines.google import GoogleEngine
from .engines.yandex import YandexEngine
from .translators import Translator, translate_engines

translate_engines.register(engine=BingEngine)
translate_engines.register(engine=GoogleEngine)
translate_engines.register(engine=YandexEngine)

__all__ = [
    'translate_engines',
    'Translator',
    '__version__',
]
