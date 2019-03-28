from .engine import BaseEngine

import typing as t


class Translator:
    """
    The MAIN interface of this package.

    It has knowledge of engines, their types, their responses and response handlers.
    It delegates responsibility to communicate with real outer translation services to engines.
    It doesn't handle a translation service response on his own, it delegates it to an instance of `ResponseHandler`.

    >>> translator = Translator.get_translator('yandex', api_key='some_key')
    >>> translator.get_languages()
    ['en', 'ru']
    >>> translator.is_language_supported('en')
    True
    >>> translator.translate(source='en', target='es', text='Hello, word!')
    'Hola palabra'
    """
    def __init__(self, engine: t.Type['BaseEngine'], config: dict):
        self._engine = engine(**config)

    def get_languages(self) -> t.List[str]:
        response = self._engine.get_langs()
        # NOTE: if some error occurs ResponseHandler::resolve_get_langs(...) should resolve it too
        return self._response_handler.resolve_get_langs(response)

    def translate(self, *, source: str, target: str, text: str) -> str:
        response = self._engine.translate(source=source, target=target, text=text)
        return self._response_handler.resolve_translate(response)

    @classmethod
    def get_translator(cls, translate_machine_name: str, *, api_key: str) -> 'Translator':
        # it's how in python the factory pattern looks like

        if translate_machine_name not in tm_receptionist:
            raise YouScrewedUpError

        translate_machine, response_handler = tm_receptionist[translate_machine_name]  # TODO
        return cls(translate_machine=translate_machine, response_handler=response_handler)


class TranslatorFactory:  # TODO: rename it to `TranslateMachine`
    """
    Translate Machine Receptionist is an object that register translation machines and their handlers.

    >>> from translate_wrapper.tm_receptionist import tm_receptionist
    >>> from translate_wrapper.yandex import YandexEngine as YandexTranslationMachine
    >>> from translate_wrapper.response_handlers import YandexResponseHandler
    >>> tm_receptionist.register(machine=YandexTranslationMachine, response_handler=YandexResponseHandler)
    >>> from translate_wrapper.google import GoogleEngine
    >>> tm_receptionist.register(machine=GoogleEngine)  # ok
    """

    def __init__(self):
        self._translators = {}

    # TODO: implement it
    def register(self, *, machine: t.Type['BaseEngine'],
                 response_handler: t.Optional[t.Type['BaseResponseHandler']] = None):
        response_handler = default_response_handler if response_handler is None else response_handler
        pass

    def register_translator(self, name: str, implementation: BaseEngine, config: t.Dict):
        self._translators[name] = Translator(implementation, config)

    def get_translator(self, name: str):
        translator = self._translators.get(name)
        if not translator:
            raise ValueError(name)
        return translator


tm_receptionist = TranslatorFactory()
del TranslatorFactory  # TODO: you can skip it
