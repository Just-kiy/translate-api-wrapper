import typing as t  # TODO


class BaseEngine:
    """
    Base class for all translate machines.

    All subclasses should be able to interact with an appropriate translation service.
    In other words, all children have only one responsibility: interaction via HTTP.

    All specific settings instances of `TranslateMachine` should get from ENV.
    """
    def __init__(self, **kwargs):
        pass

    def translate(self, **kwargs):
        raise NotImplementedError

    def get_langs(self, **kwargs):
        raise NotImplementedError

    def _send_request(self, **kwargs):
        raise NotImplementedError

    def convert_response(self, **kwargs):
        # TODO: it messes all up, it's not good that an engine can know the strategy how to convert a response
        raise NotImplementedError


class BaseResponseConverter:
    def __init__(self, response):
        self.status = response.status
        self.reason = response.reason
        self.method = response.method
        self.url = response.url
        self.headers = response.headers
