from setuptools import setup
from poloniex import __author__, __email__, __version__, __license__

setup(
    name='Poloniex',
    version=__version__,
    description='(Unofficial) Poloniex.com API written in Python 3, supports Streaming, and API calls.',
    author=__author__,
    author_email=__email__,
    url='https://github.com/a904guy/poloniex-python3',
    license=__license__,
    packages=['poloniex'],
    package_dir={'Poloniex': 'poloniex'},
    test_suite='tests',
    install_requires=['autobahn', 'configObj', 'requests', 'ratelimiter']
)
