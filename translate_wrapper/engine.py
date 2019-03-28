

class BaseEngine:
    def translate(self, **kwargs):
        raise NotImplementedError

    def get_langs(self, **kwargs):
        raise NotImplementedError

    def _send_request(self, **kwargs):
        raise NotImplementedError

    def convert_response(self, **kwargs):
        raise NotImplementedError

class BaseResponseConverter:
    def __init__(self, response):
        self.status = response.status
        self.reason = response.reason
        self.method = response.method
        self.url = response.url
        self.headers = response.headers
