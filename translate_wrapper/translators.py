import typing as t

import asyncio

from .engines.engine import BaseEngine


class Translator:
    """
    The MAIN interface of this package.

    It has knowledge of engines, their types, their responses and response handlers.
    It delegates responsibility to communicate with real outer translation services to engines.

    >>> translator = Translator.get_translator('yandex', api_key='some_key')
    >>> translator.get_languages('es')  # NOTE: (Only BCP-47 codes!)
    ['en', 'ru']
    >>> translator.translate(source='en', target='es', text='Hello, word!')
    'Hola palabra'

    >>> translate.translate(source='en', target='es', text='Hello, word!')


    >>> translate.translate('hello <div bla=1/> mr black', 'bla')
    'привет <div bla=1/> мистер блэк'
    """
    def __init__(self, engine: t.Type['BaseEngine'], config: dict):
        self._engine = engine(**config)

    def get_languages(self, target_language: t.Optional[str]) -> t.List[str]:
        response = self._engine.get_languages(target_language)
        return asyncio.run(response)

    def translate(self, *text: str, source: t.Optional[str], target: str) -> t.List[str]:
        response = self._engine.translate(source=source, target=target, text=text)
        for chunk in funcy.chunk(*text, chunk_size=10):
            pass
        return asyncio.run(response)

    @classmethod
    def get_translator(cls, translator_name: str, api_key: str) -> 'Translator':

        assert translator_name in translate_engines, \
            f"{translator_name} is not registered Translate Engine! Use translate_engines.register first."

        engine = translate_engines[translator_name]
        return cls(engine=engine, config={'api_key': api_key})


class _TranslateEngines:
    """
    Translate Engines is an object that register translation engines for factory purposes.

    >>> from translate_wrapper.translators import translate_engines
    >>> from translate_wrapper.engines.yandex import YandexEngine
    >>> translate_engines.register(translator_name='Yandex', engine=YandexEngine)
    >>> from translate_wrapper.engines.google import GoogleEngine
    >>> translate_engines.register(translator_name='Google', engine=GoogleEngine)  # ok
    """

    def __init__(self):
        self._translator_machines = {}

    def __contains__(self, item):
        return item in self._translator_machines

    def __getitem__(self, key):
        return self._translator_machines[key]

    def register(self, *, translator_name: str, engine: t.Type['BaseEngine']):
        self._translator_machines[translator_name] = engine


translate_engines = _TranslateEngines()
