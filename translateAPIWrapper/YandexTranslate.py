from Engine import BaseEngine
import requests
from pprint import pprint


class YandexEngine(BaseEngine):
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint_api = "https://translate.yandex.net/api/v1.5/tr.json"

    def _send_request(self, url, body=None):
        request = requests.post(url, body)
        return request.text

    def translate(self, text, lang, format="plain"):
        url = "{api}/translate?" \
                "key={key}&lang={lang}&format={format}".format(
                    api=self.endpoint_api,
                    key=self.api_key,
                    lang=lang,
                    format=format)
        body = {"text": text}
        return self._send_request(url, body)

    def get_langs(self, lang):
        url = "{api}/getLangs?" \
            "key={key}& \ ui={lang}".format(
                    api=self.endpoint_api,
                    key=self.api_key,
                    lang=lang)
        return self._send_request(url)


class YandexServiceBuilder():
    def __init__(self):
        self._instance = None

    def __call__(self, api_key):
        if not self._instance:
            self._instance = YandexEngine(api_key)
        return self._instance
