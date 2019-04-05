import asyncio

from environs import Env

from translate_wrapper.engines.yandex import YandexEngine
from translate_wrapper.translators import Translator, translate_engines

from translate_wrapper.research.utils import read_from_file

TEST_TEXT = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty',
    'twenty one', 'twenty two'
]


async def main():
    text = read_from_file('resource.txt')
    translate_engines.register(translator_name='Yandex', engine=YandexEngine)
    yandex_translator = Translator.get_translator('Yandex', env.str('YANDEX_API_KEY'))
    langs = await yandex_translator.get_languages('ru')
    translate_one_string = await yandex_translator.translate('one', source='en', target='ru')
    translate_list_one = await yandex_translator.translate(TEST_TEXT, source='en', target='ru')
    translate_list_two = await yandex_translator.translate(text, source='en', target='ru')
    print(langs)
    print(translate_one_string)
    print(translate_list_one)
    print(translate_list_two)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
