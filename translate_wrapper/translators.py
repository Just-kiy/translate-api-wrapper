from .bing import BingServiceBuilder
from .engine import ObjectFactory
from .google import GoogleServiceBuilder
from .yandex import YandexServiceBuilder

factory = ObjectFactory()
factory.register("Yandex", YandexServiceBuilder())
factory.register("Google", GoogleServiceBuilder())
factory.register("Bing", BingServiceBuilder)
