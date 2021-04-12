# coding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvcdr_jiangshan00000",
    version="0.0.1",
    author="jiangshan00000",
    author_email="710806594@qq.com",
    description="A vcd wave file read library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jiangshan00001/pyvcdr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)