import typing as t

from .engine import BaseEngine


class Translator:
    """
    The MAIN interface of this package.

    It has knowledge of engines, their types, their responses and response handlers.
    It delegates responsibility to communicate with real outer translation services to engines.
    It doesn't handle a translation service response on his own, it delegates it to an instance of `ResponseHandler`.

    >>> translator = Translator.get_translator('yandex', api_key='some_key')
    >>> translator.get_languages()
    ['en', 'ru']
    >>> translator.translate(source='en', target='es', text='Hello, word!')
    'Hola palabra'
    """
    def __init__(self, engine: t.Type['BaseEngine'], config: dict):
        self._engine = engine(**config)

    def get_languages(self, target_language: t.Optional[str]) -> t.List[str]:
        response = self._engine.get_languages(target_language)
        return response

    def translate(self, *, source: str, target: str, text: str) -> t.List[str]:
        response = self._engine.translate(source=source, target=target, text=text)
        return response

    @classmethod
    def get_translator(cls, translate_machine_name: str, *, api_key: str) -> 'Translator':
        # TODO: Errors
        if translate_machine_name not in tm_receptionist:
            raise YouScrewedUpError

        translate_machine = tm_receptionist[translate_machine_name]
        return cls(translate_machine=translate_machine)


class TranslatorMachine:
    # TODO: update docstring after all
    """
    Translate Machine Receptionist is an object that register translation machines and their handlers.

    >>> from translate_wrapper.tm_receptionist import tm_receptionist
    >>> from translate_wrapper.yandex import YandexEngine as YandexEngine
    >>> tm_receptionist.register(machine=YandexEngine)
    >>> from translate_wrapper.google import GoogleEngine
    >>> tm_receptionist.register(machine=GoogleEngine)  # ok
    """

    def __init__(self):
        self._translator_machines = {}

    def __contains__(self, item):
        return item in self._translator_machines

    def __getitem__(self, key):
        return self._translator_machines[key]

    # TODO: implement it
    def register(self, *, machine: t.Type['BaseEngine']):
        self._translator_machines[machine]


tm_receptionist = TranslatorMachine()
del TranslatorMachine  # TODO: you can skip it
