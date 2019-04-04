import asyncio
from pprint import pprint

from environs import Env

from translate_wrapper.engines.bing import BingEngine
from translate_wrapper.translators import Translator, translate_engines

from translate_wrapper.research.utils import read_from_file

TEST_TEXT = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty',
    'twenty one', 'twenty two'
]


async def main():
    text = read_from_file('resource.txt')
    translate_engines.register(translator_name='Bing', engine=BingEngine)
    bing_translator = Translator.get_translator('Bing', env.str('BING_API_KEY'))
    langs = await bing_translator.get_languages('ru')
    translate_one_string = await bing_translator.translate('one', source='en', target='ru')
    translate_list_one = await bing_translator.translate(TEST_TEXT, source='en', target='ru')
    translate_list_two = await bing_translator.translate(text, source='en', target='ru')
    pprint(langs)
    pprint(translate_one_string)
    pprint(translate_list_one)
    pprint(translate_list_two)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
