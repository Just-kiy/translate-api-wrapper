=====================
Wrapper-api-translate
=====================

Library that wraps the most popular translate API's.
Currently implemented Yandex Translate, Bing and Google is under development

Install
_______
.. code-block:: console

    $ pip install -e git+https://github.com/Just-kiy/translate-api-wrapper.git

Usage
_____

.. code-block:: python

    import aiohttp
    import asyncio

    from translate_wrapper import YandexEngine

    YANDEX_API_KEY="PASTE_YOUR_API_KEY_HERE"

    engine = YandexEngine(YANDEX_API_KEY)

    async def main():
        async with aiohttp.ClientSession() as session:

            #Getting available langs for given language
            langs = await engine.get_langs("ru")

            #Translate from lang to lang
            translate1 = await engine.translate("Hello, world!", "en-ru")

            # Detect lang and translate to given lang
            translate2 = await engine.translate("Hello, world!", "ru")
            print(langs.body)
            print(translate1.body)
            print(translate2.body)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

Requirements
============
* aiohttp_
* Python_ >=3.6

.. _Python: https://www.python.org
.. _aiohttp: https://github.com/aio-libs/aiohttp

