from setuptools import setup, find_packages
from translate_wrapper import __version__

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name="wrapper-api-translate",
    description="Wrapper to popular translate APIs",
    long_description=readme(),
    version=__version__,
    url='https://github.com/Just-kiy/translate-api-wrapper',
    packages=find_packages(),
    author='Just_kiy',
    author_email="just13kiy@gmail.com",
    test_suite="tests",
    license="MIT",
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=['aiohttp>=3.3.2']
)