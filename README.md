[![pipeline status](https://gitlab.marfa-dev.space/marfa/translate-api-wrapper/badges/develop/pipeline.svg)](https://gitlab.marfa-dev.space/marfa/translate-api-wrapper/commits/develop)
[![coverage report](https://gitlab.marfa-dev.space/marfa/translate-api-wrapper/badges/develop/coverage.svg)](https://gitlab.marfa-dev.space/marfa/translate-api-wrapper/commits/develop)

# Translate API Wrapper


Library that wraps the most popular translate API's.
Currently implemented Yandex Translate, Bing and Google.

## Install

    $ pip install -e git+https://github.com/Just-kiy/translate-api-wrapper.git

## Usage

    import asyncio
  
    from translate_wrapper.translators import Translator
    
    async def main():
        api_key = os.getenv('Put here your engine's api key env')
        translator = await Translator.get_translator('name of the engine you want to use', api_key)
        # NOTE: name should be in ['Yandex', 'Google', 'Bing']
        
        source_language = 'en' # NOTE: all languages should be represented in BCP-47 codes 
        languages = translator.get_languages(source_language)
        
        text = 'Hello'
        big_text = ['This is first string', 'This is second one']
        
        translations = []
        for target_language in languages:
            translation += await translator.translate(text, source=source_language, target=target_language)
            translation += await translator.translate(*big_text, source=source_language, target=target_language)
                  
            # NOTE: You can specify how many lines translator will try to process in one request
            # to speed up performance - chunk_size parameter (default is 10)
             
        print(translations)

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
            
## Requirements

* [Python](https://www.python.org/) >=3.6
* [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
* [funcy](https://funcy.readthedocs.io/en/stable/index.html)


