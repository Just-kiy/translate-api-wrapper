import typing as t


class BaseEngineError(Exception):
    def get_template(self):
        raise NotImplementedError

    def __str__(self):
        return self.detail


class EngineGetLangsError(BaseEngineError):
    def __init__(self, service_name: str = '',
                 code: str = None,
                 msg: t.Dict = None):
        self.original_response = msg
        self.detail = self.get_template().format(service_name, code, parameter, str(msg))

    def get_template(self):
        return '{service_name}-{code}: ' \
               'failed to get available languages. Original message: {msg}.'


class EngineTranslationError(BaseEngineError):
    def __init__(self, service_name: str = '', code: str = None,
                 msg: t.Dict = None):
        self.original_response = msg
        self.detail = self.get_template().format(service_name, code, text, source, target, str(msg))

    def get_template(self):
        return '{service_name}-{code}: ' \
               'Translation error}. Original message: {msg}.'
