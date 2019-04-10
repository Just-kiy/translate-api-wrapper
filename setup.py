from setuptools import setup, find_packages
from translate_wrapper import __version__


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name="translate-api-wrapper",
    author='Just_kiy',
    author_email="just13kiy@gmail.com",
    description="Wrapper to popular translate APIs",
    long_description=readme(),
    version=__version__,
    url='https://github.com/Just-kiy/translate-api-wrapper',
    packages=find_packages(),
    test_suite="tests",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['aiohttp>=3.3.2']
)
