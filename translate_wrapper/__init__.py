__version__ = '0.4.0'

from .engines.bing import BingEngine
from .engines.google import GoogleEngine
from .engines.yandex import YandexEngine
from .translators import translate_engines, Translator

translate_engines.register(engine=BingEngine)
translate_engines.register(engine=GoogleEngine)
translate_engines.register(engine=YandexEngine)

__all__ = [
    'translate_engines',
    'Translator',
    '__version__',
]
