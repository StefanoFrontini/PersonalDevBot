try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'PersonalDevBot',
    'author': 'Stefano Frontini',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'stefanofrontini75@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['tweepy'],
    'scripts': [],
    'name': 'PersonalDevBot'

}

setup(**config)
