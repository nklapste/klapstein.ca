""" server module that defines the cherrypy server deployment add your
options mainly here """

import os

import logging
from logging import handlers

import cherrypy

from webdep import PUBDIR, LOGDIR, BACKUP_COUNT
from webdep.templates import ERROR_TEMPLATE, INDEX_TEMPLATE
from webdep.bottle_server import BOTTLE_APP


# get instance of general server log
__log__ = logging.getLogger("general")


def error_page(status, message, traceback, version):
    """ custom error with jinja templating capability for the cherrypy server"""
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
        """ home page """
        return INDEX_TEMPLATE.render()


def setup_logging(logdir):
    """ setup cherrypy logging to be more advanced having a
    rotating file handler and logging to an internal directory """
    log = cherrypy.log

    # Remove the default FileHandlers if present.
    log.error_file = ""
    log.access_file = ""

    # Make a new RotatingFileHandler for the error log.
    logpath = os.path.join(logdir, "error.log")
    h = handlers.TimedRotatingFileHandler(logpath, "D",
                                          backupCount=BACKUP_COUNT)
    h.setLevel(logging.DEBUG)
    h.setFormatter(cherrypy._cplogging.logfmt)
    log.error_log.addHandler(h)

    # Make a new RotatingFileHandler for the access log.
    logpath = os.path.join(logdir, "access.log")
    h = handlers.TimedRotatingFileHandler(logpath, "D",
                                          backupCount=BACKUP_COUNT)
    h.setLevel(logging.DEBUG)
    h.setFormatter(cherrypy._cplogging.logfmt)
    log.access_log.addHandler(h)


def start_server(host="127.0.0.1", port=9091, logdir=LOGDIR):
    """ start the cherrypy server """
    config = {
        "global": {
            "server.socket_host": host,
            "server.socket_port": port,
            "error_page.default": error_page,
            'engine.autoreload_on': False  # TODO REMOVE FOR RELEASE
        },
        "/": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": PUBDIR,
            "tools.sessions.on": True,
        }
    }

    __log__.info("server startup with config: {}".format(config))

    # setup cherrypy logging in detail (adding rotating file handler logging)
    setup_logging(logdir)

    # start cherrypy server
    cherrypy.quickstart(
        Root(),
        "/",
        config=config
    )


def start_bottle_server(host="127.0.0.1", port=9091, logdir=LOGDIR):
    """ start the cherrypy server with a bottle server grafted on it """
    config = {
        "global": {
            "server.socket_host": host,
            "server.socket_port": port,
            "error_page.default": error_page,
            'engine.autoreload_on': False  # TODO REMOVE FOR RELEASE
        },
        "/": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": PUBDIR,
            "tools.sessions.on": True,
        }
    }
    # setup cherrypy logging in detail (adding rotating file handler logging)
    setup_logging(logdir)
    cherrypy.tree.graft(BOTTLE_APP, "/")
    cherrypy.config.update(config)
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    start_bottle_server()
