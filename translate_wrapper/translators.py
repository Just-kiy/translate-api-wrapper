from .engine import BaseEngine


class TranslatorFactory:
    _engines = {}

    def register_engine(self, name: str, implementation: BaseEngine):
        self._engines[name] = implementation

    def get_translator(self, name: str):
        translator = self._engines.get(name)
        if not translator:
            raise ValueError(name)
        return translator
