import asyncio

from environs import Env

import logging
import logging.config

from translate_wrapper.engines.google import GoogleEngine
from translate_wrapper.translators import Translator, translate_engines

from research.utils import read_from_file

TEST_TEXT = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty',
    'twenty one', 'twenty two'
]


async def main(env):
    logging.config.fileConfig('/home/user/projects/translate-api-wrapper/logging.conf')
    logger = logging.getLogger('GoogleTest')

    logger.info('Going to read text from file')
    text = read_from_file('resource.txt')
    logger.info('Creating translator')
    translate_engines.register(translator_name='Google', engine=GoogleEngine)
    google_translator = Translator.get_translator('Google', env.str('GOOGLE_API_KEY'))

    logger.info('Pulling languages from Service')
    langs = await google_translator.get_languages('ru')
    logger.info('Pulling languages from Service - DONE')

    logger.info('Translating one string')
    translate_one_string = await google_translator.translate('one', source='en', target='ru')
    logger.info('Translating one string - DONE')

    logger.info('Translating test list')
    translate_list_one = await google_translator.translate(*TEST_TEXT, source='en', target='ru')
    logger.info('Translating test list - DONE')

    logger.info('Translating real file example')
    translate_list_two = await google_translator.translate(*text, source='en', target='ru', chunk_size=8)
    logger.info('Translating real file example - DONE')

    print(langs)
    print(translate_one_string)
    print(translate_list_one)
    # print(translate_list_two)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(env))
