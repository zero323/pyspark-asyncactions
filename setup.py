import sys
from setuptools import setup, find_packages


install_requires = [] if sys.version_info >= (3, 2) else ["futures"]

setup(
    name='asyncactions',
    version='0.0.1',
    packages=find_packages("."),
    url='https://github.com/zero323/pyspark-async-actions',
    license='Apache 2.0',
    author='zero323',
    author_email='',
    description='A proof of concept asynchronous actions for PySpark using concurent.futures',
    long_description=(open('README.md').read() if exists('README.md')
                        else ''), 
    install_requires=install_requires
)
