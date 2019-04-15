import typing as t
from aiohttp import ClientSession

class BaseEngine:

    """
    Base class for all translate machines.

    All subclasses should be able to interact with an appropriate translation service.

    All subclasses should have aiohttp.ClientSession as attribute to speed up performance.
    Btw, subclasses can still use session context manager (async with) instead.
    If ClientSession is an attribute, then subclass must implement 'release' method to close session gracefully.

    All specific settings instances of `TranslateEngine` should get from ENV.

    Subclasses must implement convert response strategy and method to send request to proper Translation Service
    """
    name = 'BaseEngine'

    @classmethod
    async def create(cls, api_key: str, loop=None):
        self = cls(api_key, event_loop=loop)
        self.session = ClientSession(loop=self.event_loop)
        return self

    def translate(self, text: t.Union[str, t.List[str]], target: str, source: t.Optional[str]) -> t.List[str]:
        """
        Translate given text (single string or list of strings) from source (optional) language to target one.
        :param text: string or list of strings that should be translated
        :param target: target language
        :param source: Optional - source language (usually auto-detects by Translation Service)
        :return: List of translated texts
        """
        raise NotImplementedError

    def get_languages(self, language: t.Optional[str]) -> t.List[str]:
        """
        Takes language and return list of languages (BCP-47), which are available as translate direction from given one
        :param language: Source language
        :return: List of target languages
        """
        raise NotImplementedError

    def convert_response(self, method: str, response: t.Dict) -> t.List[str]:
        """
        Wrapper. Takes method name and dispatch response to it
        :param (Str) method: 'get_langs'|'translate"
        :param (Dict) response: JSON from Translation Service
        :return: (List) Converted response
        """
        raise NotImplementedError
