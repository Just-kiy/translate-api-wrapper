import typing as t


class TranslateWrapperBaseError(Exception):
    pass


class BaseEngineError(TranslateWrapperBaseError):
    detail: str = 'Error!'

    def get_template(self):
        raise NotImplementedError

    def __str__(self):
        return self.detail


class TranslationServiceError(BaseEngineError):
    def __init__(self, service_name: str = '', code: t.Optional[str] = None, msg: t.Optional[dict] = None):
        self.original_response = msg
        self.detail = self.get_template().format(service_name=service_name, code=code, msg=str(msg))

    def get_template(self):
        return '{service_name}-{code}. Message from server: {msg}'
