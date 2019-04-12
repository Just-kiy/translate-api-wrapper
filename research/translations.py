import datetime
import logging
import logging.config
import os
import typing as t
from pathlib import Path
from sys import argv
from statistics import mean, median
import asyncio

from environs import Env

from translate_wrapper.translators import Translator

if t.TYPE_CHECKING:
    from translate_wrapper.engines import BaseEngine


def read_from_file(filename: str):
    result = []
    with open(filename) as f:
        for line in f:
            result.append(line)
    return result

TEST_TEXT = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty',
    'twenty one', 'twenty two'
]

BASE_PATH = Path('.').absolute()


async def make_research(env: 'Env', chunk_size: int, *engines: 'BaseEngine'):
    logging.config.fileConfig(os.path.join(BASE_PATH, 'logging.conf'))
    logger = logging.getLogger('Research')

    logger.debug('Going to read text from file')
    text = read_from_file(os.path.join(BASE_PATH, 'research/resource.txt'))

    for engine_name in engines:
        logger.info(f'Creating {engine_name} translator')
        translator = Translator.get_translator(engine_name, env.str(f'{engine_name.upper()}_API_KEY'))

        logger.info(f'{engine_name}: Translating one string')
        start = datetime.datetime.now()
        await translator.translate('one', source='en', target='ru', chunk_size=chunk_size)
        logger.info(f'DONE - Took {datetime.datetime.now()-start} time')

        logger.info(f'{engine_name}: Translating test list')
        start = datetime.datetime.now()
        await translator.translate(*TEST_TEXT, source='en', target='ru', chunk_size=chunk_size)
        logger.info(f'DONE - Took {datetime.datetime.now()-start} time')

        logger.info(f'{engine_name}: Translating real file example from resourse.txt')
        start = datetime.datetime.now()
        await translator.translate(*text, source='en', target='ru', chunk_size=chunk_size)
        logger.info(f'DONE - Took {datetime.datetime.now()-start} time')

        logger.info(f'{engine_name}: x10 resourse.txt')
        timespans = []
        for i in range(10):
            logger.info(f'Attempt {i} of 10:')
            start = datetime.datetime.now()
            await translator.translate(*text, source='en', target='ru', chunk_size=chunk_size)
            stop = datetime.datetime.now()
            timespans.append(stop-start)
            logger.info(f'DONE - Took {stop-start} time')
        logger.info(f'DONE - x10, average: {mean(timespans)}, median: {median(timespans)}')

        logger.info(f'{engine_name}: x100 resourse.txt')
        text *= 10
        start = datetime.datetime.now()
        await translator.translate(*text, source='en', target='ru', chunk_size=chunk_size)
        logger.info(f'DONE - Took {datetime.datetime.now()-start} time')

        logger.info(f'{engine_name}: Made full research')


if __name__ == '__main__':
    env = Env()
    env.read_env()
    engines = ['Google', 'Yandex', 'Bing']
    chunk_size = 5
    if len(argv) > 1:
        engines = [argv[1].capitalize()]
    if len(argv) > 2:
        chunk_size = int(argv[2])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_research(env, chunk_size, *engines))
