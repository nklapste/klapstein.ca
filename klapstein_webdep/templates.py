#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""Module that handles the initialization and formatting of various jinja2
templates"""

from jinja2 import Environment, FileSystemLoader

from klapstein_webdep import WEB_DIR


TEMPLATE_ENV = Environment(loader=FileSystemLoader(WEB_DIR))
INDEX_TEMPLATE = TEMPLATE_ENV.get_template("index.html")
ERROR_TEMPLATE = TEMPLATE_ENV.get_template("error.html")
