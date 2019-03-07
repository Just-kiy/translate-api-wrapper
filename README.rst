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

    import translate_wrapper

    yandex = translate_wrapper.YandexEngine(*YOUR_API_KEY*)

    #Getting available langs
    yandex.get_langs('ru')

    #Translate from lang to lang
    yandex.translate('Hello', 'en-ru')
    
    #Detect lang and translate to given lang
    yandex.translate('Hello', 'ru')

Requirements
============
* aiohttp_
* Python_ >=3.6

.. _Python: https://www.python.org
.. _aiohttp: https://github.com/aio-libs/aiohttp

