import typing as t


class TranslateWrapperBaseError(Exception):
    pass


class BaseEngineError(TranslateWrapperBaseError):
    detail: str = 'Ahtung'

    def get_template(self):
        raise NotImplementedError

    def __str__(self):
        return self.detail


class EngineGetLangsError(BaseEngineError):
    tmp = ''
    
    def __init__(self, service_name: str = '',
                 code: str = None,
                 msg: t.Dict = None):
        self.original_response = msg
        self.detail = self.get_template().format(service_name=service_name, code=code, msg=str(msg))

    def get_template(self):
        return '{service_name}-{code}: ' \
               'failed to get available languages. Original message: {msg}.'


class EngineTranslationError(BaseEngineError):
    def __init__(self, service_name: str = '', code: str = None,
                 msg: t.Dict = None):
        self.original_response = msg
        self.detail = self.get_template().format(service_name=service_name, code=code, msg=str(msg))

    def get_template(self):
        return '{service_name}-{code}: ' \
               'Translation error. Original message: {msg}.'
