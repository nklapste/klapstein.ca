#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""Server module that defines the cherrypy server deployment add your
options mainly here"""

import logging

import cherrypy

from klapstein_webdep import PUB_DIR
from klapstein_webdep.templates import ERROR_TEMPLATE, INDEX_TEMPLATE


__log__ = logging.getLogger(__name__)


def error_page(status, message, traceback, version):
    """Custom error with jinja templating capability for the cherrypy server"""
    error_vars = {
        "status": status,
        "message": message,
        "traceback": traceback,
        "version": version
    }
    return ERROR_TEMPLATE.render(error_vars)


class Root(object):

    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        """Home page"""
        return INDEX_TEMPLATE.render()


def start_server(host="127.0.0.1", port=9091, cert=None,
                 key=None, bundle=None):
    """Start the cherrypy server"""
    config = {
        "global": {
            "server.socket_host": host,
            "server.socket_port": port,
            "error_page.default": error_page,
            "engine.autoreload.on": False,  # TODO REMOVE FOR RELEASE
            "server.ssl_module": "builtin",
            "server.ssl_certificate": cert,
            "server.ssl_private_key": key,
            "server.ssl_certificate_chain": bundle,
        },
        "/": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": PUB_DIR,
            "tools.sessions.on": True,
        }
    }

    __log__.info("server startup with config: {}".format(config))

    # start cherrypy server
    cherrypy.quickstart(
        Root(),
        "/",
        config=config
    )
