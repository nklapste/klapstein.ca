#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""klapstein.ca web deployment setup"""

import sys
import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        os.makedirs("test-reports", exist_ok=True)
        open("pytest.log", "w").close()
        self.pytest_args = "-v --log-file=test-reports/pytest.log " \
                           "--log-format='%(asctime)s %(levelname)s %(message)s' " \
                           "--log-date-format='%Y-%m-%d %H:%M:%S'"

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


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
    tests_require=["pytest",],
    entry_points={
        "console_scripts": ["start-klapsteinca=klapstein_webdep.__main__:main"],
    },
    cmdclass={'test': PyTest},
)