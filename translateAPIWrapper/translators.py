from Engine import ObjectFactory
from YandexTranslate import YandexServiceBuilder

factory = ObjectFactory()
factory.register("Yandex Translate", YandexServiceBuilder())
