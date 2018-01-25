""" module that handles the initialization and formatting of various jinja2
templates """

from jinja2 import Environment, FileSystemLoader

from webdep import WEBDIR


TEMPLATE_ENV = Environment(loader=FileSystemLoader(WEBDIR))
INDEX_TEMPLATE = TEMPLATE_ENV.get_template("index.html")
ERROR_TEMPLATE = TEMPLATE_ENV.get_template("error.html")
