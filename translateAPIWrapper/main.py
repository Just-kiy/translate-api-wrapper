from translators import factory

if __name__ == "__main__":
    ya_config = {
        "api_key": "trnsl.1.1.20190221T131631Z.1acbec869a7303cf.9b1b624de49bf0b1bd8bf754f0ba6a418881a90f",
    }

    ya_translate = factory.create("Yandex Translate", **ya_config)
    ya_translate.get_langs('ru')
    ya_translate.translate(text="Hello world!", lang="qq")
    ya_translate.translate(text="Hello world!", lang="ru")
