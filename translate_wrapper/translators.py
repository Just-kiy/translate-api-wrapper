import logging
import typing as t

import asyncio

import funcy

if t.TYPE_CHECKING:
    from .engines.engine import BaseEngine

logger = logging.getLogger('Translator')


class Translator:
    """
    The MAIN interface of this package.

    It has knowledge of engines, their types, their responses and response handlers.
    It delegates responsibility to communicate with real outer translation services to engines.

    >>> translator = Translator.get_translator('Yandex', api_key='some_key')
    >>> translator.get_languages('es')  # NOTE: (Only BCP-47 codes!)
    ['en', 'ru']
    >>> translator.translate(source='en', target='es', text='Hello, word!')
    'Hola palabra'
    """

    def __init__(self, engine: 'BaseEngine'):
        self._engine = engine

    async def get_languages(self, target_language: t.Optional[str]) -> t.List[str]:
        logger.info(f'{self._engine.name}: Pulling languages for {target_language}')
        response = await self._engine.get_languages(target_language)
        return response

    async def translate(self, one_line_text: str, *multiline_text: str, source: t.Optional[str],
                        target: str, chunk_size: t.Optional[int] = 10) -> t.List[str]:

        text = [one_line_text, *multiline_text]
        logger.info(f'{self._engine.name}: Translating from {source} to {target}, total strings - {len(text)}')
        tasks = []

        logger.info(f'{self._engine.name}: Creating translations tasks, chunk size: {chunk_size}')
        for chunk in funcy.chunks(chunk_size, text):
            tasks.append(self._engine.translate(*chunk, source=source, target=target))

        logger.info(f'{self._engine.name}: running all tasks, tasks count = {len(tasks)}')
        results = await asyncio.gather(*tasks)

        logger.info(f'{self._engine.name}: merging translations results')
        funcy.merge(*results)
        return results

    @classmethod
    def get_translator(cls, translator_name: str, api_key: str) -> 'Translator':

        assert translator_name in translate_engines, \
            f"{translator_name} is not registered Translate Engine! Use translate_engines.register first."

        engine_class = translate_engines[translator_name]
        engine = engine_class(api_key)
        return cls(engine=engine)


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

    def register(self, *, engine: t.Type['BaseEngine']):
        self._translator_machines[engine.name] = engine


translate_engines = _TranslateEngines()
