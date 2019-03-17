

class BaseEngine:
    def translate(self, **kwargs):
        raise NotImplementedError

    def get_langs(self, **kwargs):
        raise NotImplementedError

    def _send_request(self, **kwargs):
        raise NotImplementedError


class BaseResponseConverter:
    def __init__(self, response):
        self.status = response.status
        self.reason = response.reason
        self.method = response.method
        self.url = response.url
        self.headers = response.headers


class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def register(self, name, builder):
        self._builders[name] = builder

    def create(self, name, **kwargs):
        builder = self._builders.get(name)
        if not builder:
            raise ValueError(name)
        return builder(**kwargs)
