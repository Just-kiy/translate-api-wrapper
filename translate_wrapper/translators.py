from .engine import BaseEngine

import typing as t


class Translator:
    def __init__(self, engine: BaseEngine, config: t.Dict):
        self._engine = engine(**config)

    def get_languages(self, **kwargs):
        response = self._engine.get_langs(**kwargs)
        return self._engine.convert_response(response)

    def translate(self, **kwargs):
        response = self._engine.translate(**kwargs)
        return self._engine.convert_response(response)


class TranslatorFactory:
    _translators = {}

    def register_translator(self, name: str, implementation: BaseEngine, config: t.Dict):
        self._translators[name] = Translator(implementation, config)

    def get_translator(self, name: str):
        translator = self._translators.get(name)
        if not translator:
            raise ValueError(name)
        return translator
