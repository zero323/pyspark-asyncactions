import sys
import os
from setuptools import setup, find_packages


setup(
    name="pyspark-asyncactions",
    version="0.0.3",
    packages=find_packages("."),
    url="https://github.com/zero323/pyspark-asyncactions",
    license="Apache 2.0",
    author="zero323",
    author_email="",
    description="A proof of concept asynchronous actions for PySpark using concurent.futures",
    long_description=(
        open("README.rst").read() if os.path.exists("README.rst") else ""
    ),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
    ],
)
