#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""klapstein.ca web deployment setup"""

from setuptools import setup, find_packages


def readme():
    with open("README.rst") as f:
        return f.read()


setup(
    name="klapstein-webdep",
    version="0.0.0",
    description="klapstein.ca's python CherryPy deployment",
    long_description=readme(),
    author="Nathan Klapstein",
    author_email="nklapste@ualberta.ca",
    url="https://github.com/nklapste/klapstein.ca",
    download_url="https://github.com/nklapste/klapstein.ca/",  # TODO
    license="Apache V2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    package_data={
        "": ["README.rst"],
        "klapstein_webdep": ["logs/*", "public/*", "webpages/*"]
    },
    install_requires=[
        "cherrypy",
        "jinja2",
        "bottle"
    ],
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ["start-klapstein.ca = klapstein_webdep.__main__:main"],
    },
)