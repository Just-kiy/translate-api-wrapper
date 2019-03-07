from .engine import ObjectFactory
from .yandex import YandexServiceBuilder

factory = ObjectFactory()
factory.register("Yandex Translate", YandexServiceBuilder())
