from .engine import ObjectFactory
from .yandex import YandexServiceBuilder
from .google import GoogleServiceBuilder

factory = ObjectFactory()
factory.register("Yandex", YandexServiceBuilder())
factory.register("Google", GoogleServiceBuilder())
