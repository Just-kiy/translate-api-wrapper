from engine import BaseEngine, BaseResponseConverter
import aiohttp
import asyncio

ENDPOINT_API = "https://translation.googleapis.com/language/translate/v2/"

class GoogleEngine(BaseEngine):
    def __init__(self, api_key):
        self.api_key = api_key

    def _send_request(self, url, body):
        pass

    def translate(self, text, lang):
        pass

    def get_langs(self, lang):
        pass
    