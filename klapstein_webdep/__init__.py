#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""klapstein.ca

A simple python web deployment used to quickly setup easy to modify
jinja2 and cherrypy based python servers.
"""

import os

# DIRECTORY GLOBALS
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# PUBLIC GLOBALS
PUB_DIR = os.path.join(BASE_DIR, "public")
IMG_DIR = os.path.join(PUB_DIR, "images")
JS_DIR = os.path.join(PUB_DIR, "scripts")
CONFIG_DIR = os.path.join(PUB_DIR, "config")

# WEBPAGES GLOBALS
WEB_DIR = os.path.join(BASE_DIR, "webpages")

# LOGS GLOBALS
LOG_DIR = os.path.join(BASE_DIR, "logs")
BACKUP_COUNT = 60
